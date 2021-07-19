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
Network Related Checks
"""


import configparser

from tools.conf import settings
from tools.kube_utils import kube_exec, get_pod_with_labels

from .store_result import store_result


def physical_network_check():
    """
    physical_network_check
    """
    ml2_config = neutron_ml2_config()

    physical_networks = settings.getValue('pdf_file')['physical_networks']

    type_drivers = ml2_config.get('ml2', 'type_drivers').split(',')

    flat_networks = ml2_config.get('ml2_type_flat', 'flat_networks').split(',')

    vlan_networks = []
    network_vlan_ranges = ml2_config.get('ml2_type_vlan', 'network_vlan_ranges').split(',')
    for network in network_vlan_ranges:
        vlan_networks.append(network.split(':')[0])

    result = {'category': 'network',
              'case_name': 'physical_network_check',
              'criteria': 'pass',
              'details': []
             }

    for physnet in physical_networks:

        res = {'network_name': physnet['name'],
               'type': physnet['type'],
               'criteria': 'fail'
               }

        if physnet['type'] in type_drivers:
            if physnet['type'] == 'flat':
                if physnet['name'] in flat_networks or '*' in flat_networks:
                    res['criteria'] = 'pass'
                else:
                    res['details'] = 'physical network name not found'
            if physnet['type'] == 'vlan':
                if physnet['name'] in vlan_networks:
                    res['criteria'] = 'pass'
                else:
                    res['details'] = 'physical network name not found'
        else:
            res['details'] = 'physical network type not found'

        result['details'].append(res)
        if res['criteria'] == 'fail':
            result['criteria'] = 'fail'

    store_result(result)
    return result



def neutron_ml2_config():
    """
    Returns parsed ml2 config from neutron
    """
    ovs = get_pod_with_labels("application=neutron,component=neutron-ovs-agent")
    sriov = get_pod_with_labels("application=neutron,component=neutron-sriov-agent")

    confs = get_neutron_ml2_conf_from_pod(ovs)
    confs.extend(get_neutron_ml2_conf_from_pod(sriov))

    config = configparser.ConfigParser()
    for conf in confs:
        config.read_string(conf)

    return config




def get_neutron_ml2_conf_from_pod(pod):
    """
    Reads ml2 config from neutron pod
    """
    cmd = ['ls', '/etc/neutron/plugins/ml2/']
    response = kube_exec(pod, cmd)
    files = response.rstrip("\n").split()

    response = []
    for filename in files:
        cmd = ['cat', '/etc/neutron/plugins/ml2/' + filename]
        conf = kube_exec(pod, cmd)
        response.append(conf)

    return response
