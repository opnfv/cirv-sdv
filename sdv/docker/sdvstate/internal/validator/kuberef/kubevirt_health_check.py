import logging

from tools.kube_utils import kube_api
from tools.conf import settings
from tools.result_api import rfile
from pod_health_check import pod_status, get_logs

from .store_result import store_result

def kubevirt_check():
    v1 = kube_api()
    resp = v1.list_namespace()
    ns_names = [ns.metadata.name for ns in resp.items]

    result = {'category':  'networking',
              'case_name': 'kubevirt_check',
              'criteria':  'pass',
              'details': []
             }

    if('kubevirt' in ns_names):
        result['criteria'] = 'pass'
        result['details'].append(ns_names)
        pod_list = v1.list_namespaced_pod('kubevirt')
        for pod in pod_list.items:
            pod_stats = pod_status(pod)
            if pod_stats['criteria'] == 'fail':
                pod_stats['logs'] = get_logs(pod)
                result['criteria'] = 'fail'
            result['details'].append(pod_stats)
    else:
        result['criteria'] = 'fail'
    
    store_result(result)
    return result
