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
Pod Health Checks
"""


from tools.result_api import rfile


def pod_health_check(logger, kube_api, namespace_list_to_check):
    """
    Check health of all pods and get logs of failed pods
    """

    result = {'category':  'platform',
              'case_name': 'pod_health_check',
              'criteria':  'pass',
              'details': []
             }

    for namespace in namespace_list_to_check:
        pod_list = kube_api.list_namespaced_pod(namespace)
        for pod in pod_list.items:
            pod_stats = pod_status(logger, pod)
            if pod_stats['criteria'] == 'fail':
                pod_stats['logs'] = get_logs(kube_api, pod)
                result['criteria'] = 'fail'
            result['details'].append(pod_stats)

    return result



def pod_status(logger, pod):
    """
    Check health of a pod and returns it's status as result
    """
    result = {'criteria': 'pass',
              'name': pod.metadata.name,
              'namespace': pod.metadata.namespace,
              'node': pod.spec.node_name}

    if pod.status.container_statuses is None:
        result['criteria'] = 'fail'
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
                result['criteria'] = 'fail'
                result['pod_details'] = rfile(str(pod))

    info = f'[Health: {result["criteria"]}] Name: {result["name"]}, '
    info = info + f'Namespace: {result["namespace"]}, Node: {result["node"]}'

    logger.debug(info)
    return result


def get_logs(kube_api, pod):
    """
    Collects logs of all containers in ``pod``
    """
    logs = []
    if pod.status.container_statuses is not None:
        for container in pod.status.container_statuses:
            con = {'container': container.name}
            if container.state.waiting is not None and \
               container.state.waiting.reason == 'PodInitializing':
                log = 'Not found, status: waiting, reason: PodInitializing'
            else:
                log = kube_api.read_namespaced_pod_log(name=pod.metadata.name,
                                                       namespace=pod.metadata.namespace,
                                                       container=container.name)
            con['log'] = rfile(log)
            logs.append(con)
    return logs
