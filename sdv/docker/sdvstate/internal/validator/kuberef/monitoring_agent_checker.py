"""
Monitoring agent checks
Checks for prometheus and collectd existence and health
"""

import logging
from tools.kube_utils import kube_api
from  internal.store_result import store_result
from internal.checks.pod_health_check import pod_status, get_logs

def health_checker(pod, api_instance, logger, result):
    """
    Checks the health of pod
    """
    status = []
    pod_stats = pod_status(logger, pod)

    if pod_stats['criteria'] == 'fail':
        pod_stats['logs'] = get_logs(api_instance, pod)
        result['criteria'] = 'fail'

    status.append(pod.metadata.name)
    status.append(pod_stats)
    return status

def monitoring_agent_check():
    """
    Checks existence & health of prometheus pods
    """
    api_instance = kube_api()
    namespaces = api_instance.list_namespace()
    ns_names = []

    for nspace in namespaces.items:
        ns_names.append(nspace.metadata.name)

    result = {'category':  'observability',
              'case_name': 'prometheus_check',
              'criteria':  'pass',
              'details': []
             }

    status = []
    flag = False
    logger = logging.getLogger(__name__)
    if 'monitoring' in ns_names:
        pod_details = api_instance.list_namespaced_pod('monitoring', watch=False)
        pods = pod_details.items
        for pod in pods:
            if 'prometheus' in pod.metadata.name:
                stats = health_checker(pod, api_instance, logger, result)
                status.append(stats)
                flag = True
    else:
        for name in ns_names:
            pod_details = api_instance.list_namespaced_pod(name, watch=False)
            pods = pod_details.items
            for pod in pods:
                if 'prometheus' in pod.metadata.name:
                    stats = health_checker(pod, api_instance, logger, result)
                    status.append(stats)
                    flag = True

    if flag is False:
        result['criteria'] = 'fail'

    result['details'].append(status)
    store_result(logger, result)
    return result


def collectd_check():
    """
    Checks for collectd pods present and their state of being
    """
    api_instance = kube_api()
    pod_details = api_instance.list_pod_for_all_namespaces()
    pods = pod_details.items

    result = {'category':  'observability',
              'case_name': 'collectd_check',
              'criteria':  'pass',
              'details': []
             }

    logger = logging.getLogger(__name__)

    status = []

    flag = False
    for pod in pods:
        if 'collectd' in pod.metadata.name:
            stats = health_checker(pod, api_instance, logger, result)
            status.append(stats)
            flag = True

    if flag is False:
        result['criteria'] = 'fail'

    result['details'].append(status)
    store_result(logger, result)
    return result
