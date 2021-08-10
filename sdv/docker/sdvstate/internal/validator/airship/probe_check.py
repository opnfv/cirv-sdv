# Copyright 2020 University Of Delhi.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Probe Checks
1. Readiness
2. Liveness
"""


import logging

from tools.kube_utils import kube_api
from tools.conf import settings

from .store_result import store_result


def readiness_probe_check():
    """
    Check readiness probe of all pods
    """
    api = kube_api()
    namespace_list = settings.getValue('airship_namespace_list')

    result = {'category':  'platform',
              'case_name': 'readiness_probe_check',
              'criteria':  'pass',
              'details': []
             }

    for namespace in namespace_list:
        pod_list = api.list_namespaced_pod(namespace)
        for pod in pod_list.items:
            pod_stats = {'criteria': 'pass',
                        'name': pod.metadata.name,
                        'namespace': pod.metadata.namespace,
                        'node': pod.spec.node_name,
                        'readiness_probe': []}

            for container in pod.spec.containers:
                if hasattr(container, 'readiness_probe') and container.readiness_probe!=None:
                    pod_stats['readiness_probe'].append(container.readiness_probe)
                else:
                    pod_stats['readiness_probe'].append(None)
                    result['criteria'] = 'fail'
                    pod_stats['criteria'] = 'fail'
            result['details'].append(pod_stats)

    store_result(result)
    return result

def liveness_probe_check():
    """
    Check liveness probe of all pods
    """
    api = kube_api()
    namespace_list = settings.getValue('airship_namespace_list')

    result = {'category':  'platform',
              'case_name': 'liveness_probe_check',
              'criteria':  'pass',
              'details': []
             }

    for namespace in namespace_list:
        pod_list = api.list_namespaced_pod(namespace)
        for pod in pod_list.items:
            pod_stats = {'criteria': 'pass',
                        'name': pod.metadata.name,
                        'namespace': pod.metadata.namespace,
                        'node': pod.spec.node_name,
                        'liveness_probe': []}

            for container in pod.spec.containers:
                if hasattr(container, 'liveness_probe') and container.liveness_probe!=None:
                    pod_stats['liveness_probe'].append(container.liveness_probe)
                else:
                    pod_stats['liveness_probe'].append(None)
                    result['criteria'] = 'fail'
                    pod_stats['criteria'] = 'fail'
            result['details'].append(pod_stats)

    store_result(result)
    return result
