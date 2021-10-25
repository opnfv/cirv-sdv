"""
Kubevirt Check
Checks the existence and health of kubevirt
"""

import logging
from tools.kube_utils import kube_api
from internal.checks.pod_health_check import pod_status, get_logs
from  internal.store_result import store_result

def kubevirt_check():
    """
    Checks for existence kubevirt namespace and checks health of the pods within

    """
    k8s_api = kube_api()
    namespaces = k8s_api.list_namespace()
    ns_names = []
    for nspace in namespaces.items:
        ns_names.append(nspace.metadata.name)

    result = {'category':  'platform',
              'case_name': 'kubevirt_check',
              'criteria':  'pass',
              'details': []
             }

    logger = logging.getLogger(__name__)

    if 'kubevirt' in ns_names:
        result['criteria'] = 'pass'
        result['details'].append(ns_names)
        pod_list = k8s_api.list_namespaced_pod('kubevirt')
        for pod in pod_list.items:
            pod_stats = pod_status(logger, pod)
            if pod_stats['criteria'] == 'fail':
                pod_stats['logs'] = get_logs(k8s_api, pod)
                result['criteria'] = 'fail'
            result['details'].append(pod_stats)
    else:
        result['criteria'] = 'fail'

    store_result(logger, result)
    return result
