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



import logging
from kubernetes import client, config

from tools.kube_utils import kube_api
from tools.conf import settings
from tools.result_api import result_api, rfile



def pod_health_check():
    """
    Check health of all pods and get logs of failed pods
    """
    api = kube_api()
    namespace_list = settings.getValue('airship_namespace_list')
    for namespace in namespace_list:
        pod_list = api.list_namespaced_pod(namespace)
        for pod in pod_list.items:
            result = pod_status(pod)
            if result['state'] == 'fail':
                result['logs'] = get_logs(pod)
            result_api.store(result)



def pod_status(pod):
    """
    Check health of a pod and returns it's status as result
    """
    result = {'state': 'ok',
              'kind': 'pod',
              'name': pod.metadata.name,
              'namespace': pod.metadata.namespace,
              'node': pod.spec.node_name}

    if pod.status.container_statuses is None:
        result['state'] = 'fail'
        result['pod_details'] = rfile(str(pod))
    else:
        for container in pod.status.container_statuses:
            if container.state.running is not None:
                status = 'Running'
            if container.state.terminated is not None:
                status = container.state.terminated.reason
            if container.state.waiting is not None:
                status = container.state.waiting.reason

            if status not in ('Running', 'Completed'):
                result['state'] = 'fail'
                result['pod_details'] = rfile(str(pod))

    info = f'[Health: {result["state"]}] Name: {result["name"]}, '
    info = info + f'Namespace: {result["namespace"]}, Node: {result["node"]}'

    logger = logging.getLogger(__name__)
    logger.info(info)
    return result


def get_logs(pod):
    """
    Collects logs of all containers in ``pod``
    """
    api = kube_api()
    logs = []
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:
            con = {'container': container.name}
            if container.state.waiting is not None and \
               container.state.waiting.reason == 'PodInitializing':
                log = 'Not found, status: waiting, reason: PodInitializing'
            else:
                log = api.read_namespaced_pod_log(name=pod.metadata.name,
                                                  namespace=pod.metadata.namespace,
                                                  container=container.name)
            con['log'] = rfile(log)
            logs.append(con)
    return logs
