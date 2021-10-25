"""
Node Exporter Check
"""

import logging
from tools.kube_utils import kube_api
from internal.checks.pod_health_check import pod_status, get_logs
from internal.store_result import store_result


def node_exporter_check():
    """
    Checks existence & health of node exporter pods
    """
    kube = kube_api()
    namespaces = kube.list_namespace()
    ns_names = []
    for nspace in namespaces.items:
        ns_names.append(nspace.metadata.name)

    result = {'category':  'observability',
              'case_name': 'node_exporter_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    flag = False

    logger = logging.getLogger(__name__)

    if 'monitoring' in ns_names:
        pod_list = kube.list_namespaced_pod('monitoring', watch=False)
        pods = pod_list.items
        for pod in pods:
            if 'node-exporter' in pod.metadata.name:
                pod_stats = pod_status(logger, pod)
                if pod_stats['criteria'] == 'fail':
                    pod_stats['logs'] = get_logs(kube, pod)
                    result['criteria'] = 'fail'
                status.append(pod.metadata.name)
                status.append(pod_stats)
                flag = True
    else:
        for nspace in namespaces.items:
            pod_list = kube.list_namespaced_pod(nspace.metadata.name, watch=False)
            pods = pod_list.items
            for pod in pods:
                if 'node-exporter' in pod.metadata.name:
                    pod_stats = pod_status(logger, pod)
                    if pod_stats['criteria'] == 'fail':
                        pod_stats['logs'] = get_logs(kube, pod)
                        result['criteria'] = 'fail'
                    status.append(pod.metadata.name)
                    status.append(pod_stats)
                    flag = True

    if flag is False:
        result['criteria'] = 'fail'

    result['details'].append(status)

    store_result(logger, result)
    return result
