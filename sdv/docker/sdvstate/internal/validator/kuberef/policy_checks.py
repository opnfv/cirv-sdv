"""
Policy Checks
Checks if the policies are properly configured
"""


import ast
import logging
from tools.kube_utils import kube_api
from tools.conf import settings
from  internal.store_result import store_result

def cpu_manager_policy_check():
    """
    Checks cpu manager settings
    """
    api = kube_api()
    logger = logging.getLogger(__name__)
    node_list = api.list_node()
    nodes = []

    for node in node_list:
        nodes.append(node.metadata.name)

    result = {'category':  'compute',
              'case_name': 'cpu_manager_policy_check',
              'criteria':  'pass',
              'details': []
             }

    for node in nodes:
        configz = api.connect_get_node_proxy_with_path(node, "configz")
        configz = ast.literal_eval(configz)
        res = {
            'node': node,
            'criteria':  'pass',
            'config': []
        }

        status = []

        flag = True

        cpu_manager = settings.getValue('pdf_file')['undercloud_ook']['cpu_manager']

        if cpu_manager['policy_name'] == configz['kubeletconfig']['cpuManagerPolicy']:
            if cpu_manager['policy_name'] == 'static':
                if cpu_manager['reconcile_period'] == configz['kubeletconfig']['cpuManagerReconcilePeriod']:
                    if cpu_manager['full_pcpus'] == configz['kubeletconfig']['full-pcpus-only']:
                        flag = flag and True
                else:
                    flag = flag and False
            else:
                flag = flag and True
        else:
            flag = flag and False

        if flag is False:
            res['criteria'] = 'fail'

        status.append(cpu_manager)
        res['config'] = status
        result['details'].append(res)


    if flag is False:
        result['criteria'] = 'fail'

    store_result(logger, result)
    return result

def topology_manager_policy_check():
    """
    Checks topology manager settings
    """
    api = kube_api()
    logger = logging.getLogger(__name__)
    node_list = api.list_node()
    nodes = []

    for node in node_list:
        nodes.append(node.metadata.name)


    result = {
        'category':  'compute',
        'case_name': 'topology_manager_policy_check',
        'criteria':  'pass',
        'details': []
    }

    for node in nodes:
        configz = api.connect_get_node_proxy_with_path(node, "configz")
        configz = ast.literal_eval(configz)
        res = {
            'node': node,
            'criteria':  'pass',
            'config': []
        }

        status = []

        flag = True

        topology_manager = settings.getValue('pdf_file')['undercloud_ook']['topology_manager']

        if topology_manager['policy_name'] == configz['kubeletconfig']['topologyManagerPolicy']:
            if topology_manager['scope'] == configz['kubeletconfig']['topologyManagerScope']:
                flag = flag and True
        else:
            flag = flag and False
        if flag is False:
            res['criteria'] = 'fail'

        status.append(topology_manager)
        res['config'] = status
        result['details'].append(res)

    if flag is False:
        result['criteria'] = 'fail'

    store_result(logger, result)
    return result
