# Copyright 2020 University Of Delhi.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Compute Related Checks
"""

import configparser
import json
import re
import logging

from tools.kube_utils import kube_exec, get_pod_with_labels
from tools.conf import settings
from internal import store_result


###########
# Checks
###########

def isolated_cores_check():
    """
    isolated_cores_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_isolated_cores()
    required_value = required_isolated_cores()

    result = {'category':  'compute',
              'case_name': 'isolated_cores_check',
              'details': {'traced_cores': traced_value,
                          'required_cores': required_value
                         }
             }

    if is_ranges_equals(traced_value, required_value):
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'


    store_result(logger, result)
    return result



def reserved_vnf_cores_check():
    """
    reserved_vnf_cores_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_reserved_vnf_cores()
    required_value = required_reserved_vnf_cores()

    result = {'category':  'compute',
              'case_name': 'reserved_vnf_cores_check',
              'details': {'traced_cores': traced_value,
                          'required_cores': required_value
                         }
             }

    if is_ranges_equals(traced_value, required_value):
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'


    store_result(logger, result)
    return result



def vswitch_pmd_cores_check():
    """
    vswitch_pmd_cores_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_vswitch_pmd_cores()
    required_value = required_vswitch_pmd_cores()

    result = {'category':  'compute',
              'case_name': 'vswitch_pmd_cores_check',
              'details': {'traced_cores': traced_value,
                          'required_cores': required_value
                         }
             }

    if is_ranges_equals(traced_value, required_value):
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'


    store_result(logger, result)
    return result



def vswitch_dpdk_lcores_check():
    """
    vswitch_dpdk_lcores_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_vswitch_dpdk_lcores()
    required_value = required_vswitch_dpdk_lcores()

    result = {'category':  'compute',
              'case_name': 'vswitch_dpdk_lcores_check',
              'details': {'traced_cores': traced_value,
                          'required_cores': required_value
                         }
             }

    if is_ranges_equals(traced_value, required_value):
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'


    store_result(logger, result)
    return result



def os_reserved_cores_check():
    """
    os_reserved_cores_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_os_reserved_cores()
    required_value = required_os_reserved_cores()

    result = {'category':  'compute',
              'case_name': 'os_reserved_cores_check',
              'details': {'traced_cores': traced_value,
                          'required_cores': required_value
                         }
             }

    if is_ranges_equals(traced_value, required_value):
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'


    store_result(logger, result)
    return result



def nova_scheduler_filters_check():
    """
    nova_scheduler_filters_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_nova_scheduler_filters()
    required_value = required_nova_scheduler_filters()

    result = {'category':  'compute',
              'case_name': 'nova_scheduler_filters_check',
              'details': {'traced_filters': traced_value,
                          'required_filters': required_value
                         }
             }

    if are_lists_equal(traced_value, required_value):
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'

    store_result(logger, result)
    return result



def cpu_allocation_ratio_check():
    """
    cpu_allocation_ratio_check
    """
    logger = logging.getLogger(__name__)
    traced_value = trace_cpu_allocation_ratio()
    required_value = required_cpu_allocation_ratio()

    result = {'category':  'compute',
              'case_name': 'cpu_allocation_ratio_check',
              'details': {'traced_ratio': traced_value,
                          'required_ratio': required_value
                         }
             }

    if traced_value == required_value:
        result['criteria'] = 'pass'
    else:
        result['criteria'] = 'fail'

    store_result(logger, result)
    return result








###############
# helper functions
###############



def trace_isolated_cores():
    """
    Trace isolated_cores from Airship deployment

    :return: value traced from `isolcpus` key in `/proc/cmdline`
    """
    pod = get_pod_with_labels('application=nova,component=compute')

    cmd = ['cat', '/proc/cmdline']
    proc_cmd = kube_exec(pod, cmd)

    for option in proc_cmd.split():
        if 'isolcpus' in option:
            _, isolcpus_value = split_key_value(option)
            break

    return isolcpus_value


def required_isolated_cores():
    """
    Returns value of `isolated_cpus` from platform_profile used by
    Role for worker nodes in PDF

    :return: isolated_cores value expected by the PDF
    """
    worker_role = settings.getValue('WORKER_ROLE_NAME')
    profile = get_platform_profile_by_role(worker_role)
    return profile['isolated_cpus']






def trace_reserved_vnf_cores():
    """
    Trace vnf_reserved_cores from Airship deployment

    :return: value traced from `vcpu_pin_set` key in nova.conf
    of actual deployment
    """
    try:
        config = get_nova_conf()
        vcpu_pin_set = config.get('DEFAULT', 'vcpu_pin_set')
    except (configparser.NoOptionError, configparser.MissingSectionHeaderError):
        vcpu_pin_set = ''

    return vcpu_pin_set


def required_reserved_vnf_cores():
    """
    Returns value of vnf_cores from platform_profile used by
    Role for worker nodes in PDF

    :return: vnf_reserverd_core value expected by the PDF
    """
    worker_role = settings.getValue('WORKER_ROLE_NAME')
    profile = get_platform_profile_by_role(worker_role)
    return profile['vnf_cores']






def trace_vswitch_pmd_cores():
    """
    Trace vswitch_pmd_cores from Airship deployment

    :return: value traced from `other_config:pmd-cpu-mask` in
    openvswitchdb using ovs-vsctl
    """
    ovs_pod = get_pod_with_labels('application=openvswitch,component=openvswitch-vswitchd')

    cmd = ['ovs-vsctl', '-t', '5', 'get', 'Open_vSwitch', '.', 'other_config']
    response = kube_exec(ovs_pod, cmd)

    # convert config str to json str
    match = re.findall("[a-zA-Z0-9-]+=", response)
    for key in match:
        response = response.replace(key, '"' + key[:-1] + '":')
    match = re.findall(":[a-zA-Z0-9-]+", response)
    for key in match:
        response = response.replace(key[1:], '"' + key[1:] + '"')

    config = json.loads(response)

    if 'pmd-cpu-mask' in config:
        pmd_cores = hex_to_comma_list(config['pmd-cpu-mask'])
    else:
        pmd_cores = ''

    return pmd_cores


def required_vswitch_pmd_cores():
    """
    Returns value of vswitch_pmd_cores from platform_profile used by
    Role for worker nodes in PDF

    :return: vswitch_pmd_cores value expected by the PDF
    """
    worker_role = settings.getValue('WORKER_ROLE_NAME')
    profile = get_platform_profile_by_role(worker_role)
    return profile['vswitch_pmd_cores']






def trace_vswitch_dpdk_lcores():
    """
    Trace vswitch_dpdk_lcores from Airship deployment

    :return: value traced from `other_config:dpdk-lcore-mask` in
    openvswitchdb using ovs-vsctl
    """
    ovs_pod = get_pod_with_labels('application=openvswitch,component=openvswitch-vswitchd')

    cmd = ['ovs-vsctl', '-t', '5', 'get', 'Open_vSwitch', '.', 'other_config']
    response = kube_exec(ovs_pod, cmd)

    # convert config str to json str
    match = re.findall("[a-zA-Z0-9-]+=", response)
    for key in match:
        response = response.replace(key, '"' + key[:-1] + '":')
    match = re.findall(":[a-zA-Z0-9-]+", response)
    for key in match:
        response = response.replace(key[1:], '"' + key[1:] + '"')

    config = json.loads(response)

    if 'dpdk-lcore-mask' in config:
        pmd_cores = hex_to_comma_list(config['dpdk-lcore-mask'])
    else:
        pmd_cores = ''

    return pmd_cores


def required_vswitch_dpdk_lcores():
    """
    Returns value of vswitch_dpdk_lcores from platform_profile used by
    Role for worker nodes in PDF

    :return: vswitch_dpdk_lcores value expected by the PDF
    """
    worker_role = settings.getValue('WORKER_ROLE_NAME')
    profile = get_platform_profile_by_role(worker_role)
    return profile['vswitch_dpdk_lcores']






def trace_os_reserved_cores():
    """
    Trace os_reserved_cores from Airship deployment

    os_reserved_cores = all_cores - (reserved_vnf_cores +
                                     vswitch_pmd_cores +
                                     vswitch_dpdk_lcores)
    """
    worker_role = settings.getValue('WORKER_ROLE_NAME')
    all_cores = get_cores_by_role(worker_role)

    reserved_vnf_cores = trace_reserved_vnf_cores()
    vswitch_pmd_cores = trace_vswitch_pmd_cores()
    vswitch_dpdk_lcores = trace_vswitch_dpdk_lcores()

    non_os_cores = []
    non_os_cores.extend(convert_range_to_list(reserved_vnf_cores))
    non_os_cores.extend(convert_range_to_list(vswitch_pmd_cores))
    non_os_cores.extend(convert_range_to_list(vswitch_dpdk_lcores))

    os_reserved_cores = set(all_cores).difference(set(non_os_cores))

    # return as string with comma separated value
    return ','.join(map(str, list(os_reserved_cores)))


def required_os_reserved_cores():
    """
    Returns value of os_reserved_cores from platform_profile used by
    Role for worker nodes in PDF

    :return: os_reserved_cores value expected by the PDF
    """
    worker_role = settings.getValue('WORKER_ROLE_NAME')
    profile = get_platform_profile_by_role(worker_role)
    return profile['os_reserved_cores']





def trace_nova_scheduler_filters():
    """
    Trace scheduler_filters from Airship deployment

    :return: value traced from `enabled_filters` key in nova.conf
    of actual deployment
    """
    try:
        config = get_nova_conf()
        filters = config.get('filter_scheduler', 'enabled_filters')
    except (configparser.NoOptionError, configparser.MissingSectionHeaderError):
        filters = ''

    filters = filters.split(',')
    map(str.strip, filters)

    return filters

def required_nova_scheduler_filters():
    """
    Required nova scheduler_filters by the PDF
    """
    pdf = settings.getValue('pdf_file')
    filters = pdf['vim_functional']['scheduler_filters']

    filters = filters.split(',')
    map(str.strip, filters)

    return filters







def trace_cpu_allocation_ratio():
    """
    Trace cpu_allocation_ratio from Airship deployment

    :return: value traced from `cpu_allocation_ratio` key in nova.conf
    of actual deployment
    """
    try:
        config = get_nova_conf()
        cpu_allocation_ratio = config.get('DEFAULT', 'cpu_allocation_ratio')
    except (configparser.NoOptionError, configparser.MissingSectionHeaderError):
        cpu_allocation_ratio = ''

    return float(cpu_allocation_ratio)

def required_cpu_allocation_ratio():
    """
    Required cpu_allocation_ratio by the PDF
    """
    pdf = settings.getValue('pdf_file')
    cpu_allocation_ratio = pdf['vim_functional']['cpu_allocation_ratio']

    return float(cpu_allocation_ratio)







def get_role(role_name):
    """
    Searches and returns role with `role_name`
    """
    roles = settings.getValue('pdf_file')['roles']

    for role in roles:
        if role['name'] == role_name:
            role_details = role

    return role_details


def get_platform_profile(profile_name):
    """
    Searches and returns platform_profile with `profile_name`
    """
    platform_profiles = settings.getValue('pdf_file')['platform_profiles']

    for profile in platform_profiles:
        if profile['profile_name'] == profile_name:
            profile_details = profile

    return profile_details

def get_processor_profile(profile_name):
    """
    Searches and returns processor_profile with `profile_name`
    """
    processor_profiles = settings.getValue('pdf_file')['processor_profiles']

    for profile in processor_profiles:
        if profile['profile_name'] == profile_name:
            profile_details = profile

    return profile_details

def get_platform_profile_by_role(role_name):
    """
    Returns platform profile details of a role
    """
    role = get_role(role_name)
    profile = get_platform_profile(role['platform_profile'])
    return profile


def get_hardware_profile_by_role(role_name):
    """
    Returns hardware profile details of a role
    """
    role = get_role(role_name)

    hardware_profiles = settings.getValue('pdf_file')['hardware_profiles']

    for profile in hardware_profiles:
        if profile['profile_name'] == role['hardware_profile']:
            profile_details = profile

    return profile_details


def get_cores_by_role(role_name):
    """
    Returns cpu cores list of server hardware used in the role
    """
    hardware_profile = get_hardware_profile_by_role(role_name)
    processor_profile = hardware_profile['profile_info']['processor_profile']
    profile = get_processor_profile(processor_profile)

    cpus = []

    for numa in profile['profile_info']['numas']:
        cpus.extend(convert_range_to_list(numa['cpu_set']))

    return cpus







def get_nova_conf():
    """
    Returns parsed nova.conf
    """
    pod = get_pod_with_labels('application=nova,component=compute')

    cmd = ['cat', '/etc/nova/nova.conf']
    response = kube_exec(pod, cmd)

    config = configparser.ConfigParser()
    config.read_string(response)

    return config


### cpu cores related helper function

def convert_range_to_list(x):
    """
    Returns list of numbers from given range as string

    e.g.: convert_range_to_list('3-5') will give [3, 4, 5]
    """
    # pylint: disable=C0103
    result = []
    for part in x.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
        elif part != '':
            a = int(part)
            result.append(a)
    # remove duplicates
    result = list(dict.fromkeys(result))
    return result


def is_ranges_equals(range1, range2):
    """
    Checks whether two ranges passed as string are equal

    e.g.: is_ranges_equals('2-5', '2-4,5') returns true
    """
    set1 = set(convert_range_to_list(range1))
    set2 = set(convert_range_to_list(range2))
    return set1 == set2

def are_lists_equal(list1, list2):
    """
    Checks whether two list are identicals
    """
    set1 = set(list1)
    set2 = set(list2)
    return set1 == set2



def hex_to_comma_list(hex_mask):
    """
    Converts CPU mask given in hex to list of cores
    """
    binary = bin(int(hex_mask, 16))[2:]
    reversed_binary = binary[::-1]
    i = 0
    output = ""
    for bit in reversed_binary:
        if bit == '1':
            output = output + str(i) + ','
        i = i + 1
    return output[:-1]


def comma_list_to_hex(cpus):
    """
    Converts a list of cpu cores in corresponding hex value
    of cpu-mask
    """
    cpu_arr = cpus.split(",")
    binary_mask = 0
    for cpu in cpu_arr:
        binary_mask = binary_mask | (1 << int(cpu))
    return format(binary_mask, '02x')



def split_key_value(key_value_str, delimiter='='):
    """
    splits given string into key and value based on delimiter

    :param key_value_str: example string `someKey=somevalue`
    :param delimiter: default delimiter is `=`
    :return: [ key, value]
    """
    key, value = key_value_str.split(delimiter)
    key = key.strip()
    value = value.strip()
    return key, value
