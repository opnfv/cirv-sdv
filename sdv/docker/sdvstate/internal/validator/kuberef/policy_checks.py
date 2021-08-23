import logging

from tools.kube_utils import kube_api
from tools.conf import settings
from tools.result_api import rfile
import ast, json

from .store_result import store_result


def cpu_manager_policy_check():
    """
    Checks cpu manager settings
    """
    v1 = kube_api()
    rm = v1.list_node()
    nodes = [r.metadata.name for r in rm.items]

    result = {'category':  'compute',
              'case_name': 'cpu_manager_policy_check',
              'criteria':  'pass',
              'details': []
             }

    for i in nodes:
        ret = v1.connect_get_node_proxy_with_path(i, "configz")
        ret = ast.literal_eval(ret)
        res = {
                'node': i,
                'criteria':  'pass',
                'config': []
                }

        status = []

        flag = True

        cpu_manager = settings.getValue('pdf_file')['undercloud_ook']['cpu_manager']

        if(cpu_manager['policy_name'] == ret['kubeletconfig']['cpuManagerPolicy']):
            if(cpu_manager['policy_name'] == 'static'):
                if(cpu_manager['reconcile_period'] == ret['kubeletconfig']['cpuManagerReconcilePeriod']) and (cpu_manager['full_pcpus'] == ret['kubeletconfig']['full-pcpus-only']):
                    flag = flag and True
                else:
                    flag = flag and False
            else:
                flag = flag and True
        else:
            flag = flag and False

        if(flag == False):
            res['criteria'] ='fail'

        status.append(cpu_manager)
        res['config'] = status
        result['details'].append(res)


    if(flag == False):
        result['criteria'] ='fail'

    store_result(result)
    return result


def topology_manager_policy_check():
    """
    Checks topology manager settings
    """
    v1 = kube_api()
    rm = v1.list_node()
    nodes = [r.metadata.name for r in rm.items]

    result = {'category':  'compute',
              'case_name': 'topology_manager_policy_check',
              'criteria':  'pass',
              'details': []
             }

    for i in nodes:
        ret = v1.connect_get_node_proxy_with_path(i, "configz")
        ret = ast.literal_eval(ret)
        res = {
                'node': i,
                'criteria':  'pass',
                'config': []
                }

        status = []

        flag = True

        topology_manager = settings.getValue('pdf_file')['undercloud_ook']['topology_manager']

        if(topology_manager['policy_name'] == ret['kubeletconfig']['topologyManagerPolicy'] and topology_manager['scope'] == ret['kubeletconfig']['topologyManagerScope']):
            flag = flag and True
        else:
            flag = flag and False
            
        if(flag == False):
             res['criteria'] = 'fail'
        
        status.append(topology_manager)
        res['config'] = status
        result['details'].append(res)

    if(flag == False):
        result['criteria'] ='fail'

    store_result(result)
    return result
