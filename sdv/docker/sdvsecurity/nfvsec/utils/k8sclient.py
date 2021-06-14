"""
Kubernetes cluster api helper functions
"""


import time

from kubernetes import client, config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

from kubernetes.stream import stream
import logging
from conf import settings    # pylint: disable=import-error


class K8sClient():
    """
    Class for controlling the pod through PAPI
    """

    def __init__(self):
        """
        Initialisation function.
        """
        self._logger = logging.getLogger(__name__)
        config.load_kube_config(settings.getValue('K8S_CONFIG_FILEPATH'))
        self.api = client.CoreV1Api()

    def get_pod(self, namespace, name):
        """
        Returns json details any one pod with matching label

        :param namespace: namespace to use
        :param namespace: name of the pod (Longest possible).
        :return: pod details
        """
        api_response = self.api.list_namespaced_pod(namespace)
        for pod in api_response.items:
            #print(pod.metadata.name)
            if pod.metadata.name.startswith(name):
                return pod
        return None


    def execute(self, pod, cmd):
        """
        Executes `cmd` inside `pod` and returns response
        :param pod: pod object
        :param cmd: command to execute inside pod
        :return: response from pod
        """
        response = stream(self.api.connect_get_namespaced_pod_exec,
                        pod.metadata.name, pod.metadata.namespace, command=cmd,
                        stderr=True, stdin=False, stdout=True, tty=False)
        return response
