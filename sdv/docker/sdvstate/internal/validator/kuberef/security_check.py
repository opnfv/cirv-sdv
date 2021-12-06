"""
Security Checks
"""

#pylint: disable=broad-except

import time
import logging
from tools.kube_utils import kube_api, kube_curl
from tools.kube_utils import kube_exec
from  internal.store_result import store_result

# capability check
def capability_check():
    """
    Checks if creation of pods with particular capabilties is possible
    """
    kube = kube_api()
    logger = logging.getLogger(__name__)
    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'security-capability-demo',
        },
        'spec': {
            'containers': [{
                'image': 'alpine:3.2',
                'name': 'security-capability-demo',
                'command': ["/bin/sh", "-c", "sleep 60m"],
                'securityContext': {
                    'capabilities': {
                        'drop': [
                            "ALL"
                        ],
                        'add': [
                            'NET_ADMIN', 'NET_RAW'
                        ]
                    }
                }
            }]
        }
    }
    result = {'category':  'platform',
              'case_name': 'capability_check',
              'criteria':  'pass',
              'details': []
             }
    status = []
    try:
        pod_cap = kube.create_namespaced_pod(body=pod_manifest, namespace='default')
        time.sleep(6)
        cmd = ['cat', '/proc/1/status']

        response = kube_exec(pod_cap, cmd)
        if "0000000000003000" in response:
            result['criteria'] = 'fail'
            status.append(pod_cap)
        kube.delete_namespaced_pod(name=pod_cap.metadata.name, namespace='default')

    except KeyError as error:
        status.append(error)

    except RuntimeError as error:
        status.append(error)

    except Exception as error:
        kube.delete_namespaced_pod(name=pod_cap.metadata.name, namespace='default')
        result['criteria'] = 'fail'
        status.append(error)


    result['details'].append(status)
    store_result(logger, result)
    return result

# privileges check
def privilege_check():
    """
    Checks if privileged pods are possible to created
    """
    kube = kube_api()
    logger = logging.getLogger(__name__)

    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'security-privileges-demo',
        },
        'spec': {
            'containers': [{
                'image': 'alpine:3.2',
                'name': 'security-privileges-demo',
                'command': ["/bin/sh", "-c", "sleep 60m"],
                'securityContext': {
                    'privileged': True
                }
            }]
        }
    }
    result = {'category':  'platform',
              'case_name': 'privilege_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        pod_priv = kube.create_namespaced_pod(body=pod_manifest, namespace='default')
        time.sleep(5)
        cmd = ['ps', 'aux']

        response = kube_exec(pod_priv, cmd)

        if "root" in response:
            result['criteria'] = 'fail'
            status.append(response)

        kube.delete_namespaced_pod(name=pod_priv.metadata.name, namespace='default')

    except KeyError as error:
        status.append(error)

    except RuntimeError as error:
        status.append(error)

    except Exception as error:
        kube.delete_namespaced_pod(name=pod_priv.metadata.name, namespace='default')
        result['criteria'] = 'fail'
        status.append(error)

    result['details'].append(status)

    store_result(logger, result)
    return result

# host network check
def host_network_check():
    """
    Checks if the pods can share the network with their host
    """
    kube = kube_api()
    logger = logging.getLogger(__name__)

    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'security-host-network-demo',
        },
        'spec': {
            'hostNetwork': True,
            'containers': [{
                'image': 'k8s.gcr.io/pause',
                'name': 'security-host-network-demo',
                'command': ["/bin/sh", "-c", "sleep 60m"],
            }],
            'restartPolicy': 'Always'
        }
    }
    result = {'category':  'platform',
              'case_name': 'host_network_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        pod_nw = kube.create_namespaced_pod(body=pod_manifest, namespace='default')
        time.sleep(6)

        kube.delete_namespaced_pod(name=pod_nw.metadata.name, namespace='default')
        result['criteria'] = 'fail'

    except KeyError as error:
        status.append(error)

    except RuntimeError as error:
        status.append(error)

    except Exception as error:
        kube.delete_namespaced_pod(name=pod_nw.metadata.name, namespace='default')
        result['criteria'] = 'fail'
        status.append(error)


    result['details'].append(status)

    store_result(logger, result)
    return result

# host directory as a volume check
def host_path_vol_check():
    """
    Checks if pods can be mounted to a host directory
    """
    kube = kube_api()
    logger = logging.getLogger(__name__)

    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'security-host-path-volume-demo',
        },
        'spec': {
            'hostNetwork': True,
            'containers': [{
                'image': 'k8s.gcr.io/pause',
                'name': 'security-host-path-volume-demo',
                'command': ["/bin/sh", "-c", "sleep 60m"],
            }],
            'volumes': [
                {
                    'name': 'test-vol',
                    'hostpath': {
                        'path': 'home',
                        'type': 'Directory'
                    }
                }
            ]
        }
    }
    result = {'category':  'platform',
              'case_name': 'host_path_dir_vol_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        pod_vol = kube.create_namespaced_pod(body=pod_manifest, namespace='default')

        time.sleep(5)

        kube.delete_namespaced_pod(name=pod_vol.metadata.name, namespace='default')
        result['criteria'] = 'fail'

    except KeyError as error:
        status.append(error)

    except RuntimeError as error:
        status.append(error)

    except Exception as error:
        kube.delete_namespaced_pod(name=pod_vol.metadata.name, namespace='default')
        result['criteria'] = 'fail'
        status.append(error)

    result['details'].append(status)

    store_result(logger, result)
    return result

# kubernetes api connectivity check
def k8s_api_conn_check():
    """
    Checks for connectivity from within the pod
    """

    result = {'category':  'platform',
              'case_name': 'connectivity_check',
              'criteria':  'pass',
              'details': []
             }

    status = []
    logger = logging.getLogger(__name__)

    try:
        ca_crt = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        auth_tkn = '"Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"'
        url = 'https://kubernetes.default.svc'
        response = kube_curl('-v', '--cacert', ca_crt, '-H', auth_tkn, url)

        if "Connected to kubernetes" in response:
            result['criteria'] = 'pass'
        else:
            result['criteria'] = 'fail'

        status.append(response)

    except ConnectionError as error:
        status.append(error)

    except RuntimeError as error:
        status.append(error)

    result['details'].append(status)

    store_result(logger, result)
    return result
