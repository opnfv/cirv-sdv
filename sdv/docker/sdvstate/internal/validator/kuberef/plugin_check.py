"""
CNI Plugin Check
Multi-interface CNI Check
"""

import time
import logging
from kubernetes import client
from tools.kube_utils import kube_api, kube_exec
from tools.conf import settings
from  internal.store_result import store_result

def create_daemonset(apps_instance):
    """
    Creates daemonset for the checks
    """
    manifest = {
        'apiVersion': 'apps/v1',
        'kind': 'DaemonSet',
        'metadata': {
            'name': 'plugin-check-test-set',
            'namespace': 'default'
        },
        'spec': {
            'selector': {
                'matchLabels': {
                    'name': 'alpine'
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'name': 'alpine'
                    }
                }
            },
            'spec': {
                'containers': [{
                    'name': 'alpine',
                    'image': 'alpine:3.2',
                    'command': ["sh", "-c", "echo \"Hello K8s\" && sleep 3600"],
                    'volumeMounts': [{
                        'name': 'etccni',
                        'mountPath': '/etc/cni'
                    }, {
                        'name': 'optcnibin',
                        'mountPath': '/opt/cni/bin',
                        'readOnly': True
                    }]
                }],
                'volumes': [{
                    'name': 'etccni',
                    'hostPath': {
                        'path': '/etc/cni'
                    }
                }, {
                    'name': 'optcnibin',
                    'hostPath': {
                        'path': '/opt/cni/bin'
                    }
                }],
                'tolerations': [{
                    'effect': 'NoSchedule',
                    'key': 'node-role.kubernetes.io/master',
                    'operator': 'Exists'
                }]
            }
        }
    }
    apps_instance.create_namespaced_daemon_set('default', manifest)
    time.sleep(6)


def multi_interface_cni_check():
    """
    Checks if multi interface cni is enabled
    """
    apps_instance = client.AppsV1Api()
    api_instance = kube_api()
    logger = logging.getLogger(__name__)

    result = {'category':  'network',
              'case_name': 'multi_interface_cni_check',
              'criteria':  'pass',
              'details': []
             }

    create_daemonset(apps_instance)
    pod_details = api_instance.list_namespaced_pod('default', watch=False)
    pods = pod_details.items
    status = []
    cmd = ['ls', '/etc/cni/net.d']

    for pod in pods:
        if 'plugin-check-test-set' in pod.metadata.name:
            list_of_plugin_conf = kube_exec(pod, cmd)
            list_of_plugin_conf = list_of_plugin_conf.split("\n")

            cmd3 = ['cat', list_of_plugin_conf[0]]
            multi_interface_conf = kube_exec(pod, cmd3)

            if 'multus' not in multi_interface_conf:
                result['criteria'] = 'fail'

            status.append(list_of_plugin_conf)
            status.append(multi_interface_conf)

    apps_instance.delete_namespaced_daemon_set('plugin-check-test-set', 'default')
    result['details'].append(status)
    store_result(logger, result)
    return result

def cni_plugin_check():
    """
    Checks for CNI plugins and validate against PDF
    """
    apps_instance = client.AppsV1Api()
    api_instance = kube_api()

    result = {'category':  'network',
              'case_name': 'cni_plugin_check',
              'criteria':  'pass',
              'details': []
             }

    logger = logging.getLogger(__name__)
    create_daemonset(apps_instance)
    pod_details = api_instance.list_namespaced_pod('default', watch=False)
    pods = pod_details.items
    daemon_pods = []
    status = []
    cmd = ['ls', '/opt/cni/bin']
    cni_plugins = settings.getValue('pdf_file')['vim_functional']['cnis_supported']


    for pod in pods:
        if 'plugin-check-test-set' in pod.metadata.name:
            list_of_cni_from_dir = kube_exec(pod, cmd)

            for plugin in cni_plugins:
                if plugin not in list_of_cni_from_dir:
                    result['criteria'] = 'fail'

            status.append(list_of_cni_from_dir)
            daemon_pods.append(pod.metadata.name)

    apps_instance.delete_namespaced_daemon_set('plugin-check-test-set', 'default')

    result['details'].append(daemon_pods)
    result['details'].append(status)
    store_result(logger, result)
    return result
