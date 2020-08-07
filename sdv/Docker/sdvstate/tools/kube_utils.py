

from kubernetes import client, config
from kubernetes.stream import stream

from tools.conf import settings


def load_kube_api():
    """
    """
    config.load_kube_config(settings.getValue('kube_config'))
    kube_api = client.CoreV1Api()
    settings.setValue('kube_api', kube_api)


def kube_api():
	"""
	"""
	return settings.getValue('kube_api')


def get_pod_with_labels(labels):
    """
    """
    api = kube_api()
    pod = api.list_pod_for_all_namespaces(label_selector=labels).items[0]
    return pod


def kube_exec(pod, cmd):
    """
    """
    api = kube_api()
    response = stream(api.connect_get_namespaced_pod_exec,
                      pod.metadata.name, pod.metadata.namespace, command=cmd,
                      stderr=True, stdin=False, stdout=True, tty=False)
    return response


def kube_curl(*args):
    """
    executes curl cmd in kubernetes network
    """
    args = list(args)
    args.insert(0, "curl")

    api = kube_api()
    pod = get_pod_with_labels("application=prometheus-openstack-exporter,component=exporter")

    response = kube_exec(pod, args)

    return response