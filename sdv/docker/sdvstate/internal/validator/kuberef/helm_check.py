"""
Helm 2 disabled check

Checks if the helm v2 is supported in the cluster
"""

import logging
from tools.kube_utils import kube_api
from tools.conf import settings
from  internal.store_result import store_result

def helmv2_disabled_check():
    """
    Checks for helm v2 support
    """
    result = {'category':  'platform',
              'case_name': 'helmv2_disabled_check',
              'criteria':  'pass',
              'details': []
             }
    kube = kube_api()
    logger = logging.getLogger(__name__)
    res = False
    pod_details = kube.list_pod_for_all_namespaces()
    pods = pod_details.items
    versions = settings.getValue('pdf_file')['helm_versions']
    if 'v2' in versions:
        for pod in pods:
            if 'tiller' in pod.metadata.name:
                res = True
                result['details'].append(pod)
    if res is False:
        result['criteria'] = 'fail'
    store_result(logger, result)
    return result
