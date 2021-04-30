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
Kubernetes cluster api helper functions
"""

import time

from kubernetes import client, config
from kubernetes.stream import stream

from tools.conf import settings    # pylint: disable=import-error


def load_kube_api():
    """
    Loads kubernetes api
    """
    config.load_kube_config(settings.getValue('kube_config'))
    api = client.CoreV1Api()
    settings.setValue('kube_api', api)


def kube_api():
    """
    Returns kube_api object
    """
    return settings.getValue('kube_api')


def get_pod_with_labels(labels):
    """
    Returns json details any one pod with matching labels

    :param labels: labels to find matching pod
    :return: pod details
    """
    api = kube_api()
    pod = api.list_pod_for_all_namespaces(label_selector=labels).items[0]
    return pod


def kube_exec(pod, cmd):
    """
    Executes `cmd` inside `pod` and returns response

    :param pod: pod object
    :param cmd: command to execute inside pod
    :return: response from pod
    """
    api = kube_api()
    response = stream(api.connect_get_namespaced_pod_exec,
                      pod.metadata.name, pod.metadata.namespace, command=cmd,
                      stderr=True, stdin=False, stdout=True, tty=False)
    return response


def kube_curl(*args):
    """
    executes curl cmd in kubernetes network

    :param args: comma separated list of args to pass to curl
    :return: http response
    """
    args = list(args)
    args.insert(0, "curl")


    try:
        pod = get_pod_with_labels("application=sdvstate-curl")
    except IndexError:
        create_kube_curl_pod()
        pod = get_pod_with_labels("application=sdvstate-curl")
    finally:
        response = kube_exec(pod, args)

    return response


def create_kube_curl_pod():
    """
    Create a sandbox pod(image: curlimages/curl:7.76.1) for
    curl utility inside kubernetes cluster.
    """
    print(("Creating pod sdvstate-curl..."))
    pod_manifest = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'sdvstate-curl',
            'labels': {
                'application': 'sdvstate-curl'
            }
        },
        'spec': {
            'containers': [{
                'image': 'curlimages/curl:7.76.1',
                'name': 'sdvstate-curl',
                'command': ["/bin/sh"],
                "args": [
                    "-c",
                    "while true; do sleep 5; done"
                ]
            }]
        }
    }

    api = kube_api()
    response = api.create_namespaced_pod(body=pod_manifest,
                                         namespace='default')
    # wait 1 minute or less for pod to create.
    seconds_left = 60
    while seconds_left:
        resp = api.read_namespaced_pod(name='sdvstate-curl',
                                       namespace='default')
        if resp.status.phase == 'Running':
            break
        time.sleep(3)
        seconds_left -= 3

    if seconds_left == 0:
        raise Exception("sdvstate-curl pod taking took long to create, tests failed...")


def delete_kube_curl_pod():
    """
    Cleans curl utility pod
    """
    api = kube_api()
    api.delete_namespaced_pod(name='sdvstate-curl', body={},
                              namespace='default')
