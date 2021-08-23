import logging

from tools.kube_utils import kube_api
from tools.conf import settings
from tools.result_api import rfile

from .store_result import store_result


def monitoring_agent_check():
    """
    Checks existence of prometheus pods
    """
    v1 = kube_api()
    resp = v1.list_namespace()
    ns_names = [ns.metadata.name for ns in resp.items]

    result = {'category':  'observability',
              'case_name': 'prometheus_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    flag = False

    if 'monitoring' in ns_names:
        ret = v1.list_namespaced_pod('monitoring', watch=False)
        pods = ret.items
        pod_names = [pod.metadata.name for pod in pods]
        for i in pod_names:
            if 'prometheus' in i:
                    status.append(i)
                    flag = True
            
    else:
        for i in resp.items:
            print(i)
            ret = v1.list_namespaced_pod(i.metadata.name, watch=False)
            pods =  ret.items
            pod_names = [pod.metadata.name for pod in pods]
            for j in pod_names:
                if 'prometheus' in j:
                    status.append(j)
                    flag = True

    if flag == False:
        result['criteria'] = 'fail'

    result['details'].append(status)

    store_result(result)
    return result


    