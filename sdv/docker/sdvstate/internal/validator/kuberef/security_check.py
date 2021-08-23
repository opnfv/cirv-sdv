import yaml, time
import logging
from tools.kube_utils import kube_api, kube_curl
from tools.conf import settings
from tools.result_api import rfile
from tools.conf import settings
from tools.kube_utils import kube_exec
from .store_result import store_result



# capability check
def capability_check():
    v1 = kube_api()
    cap = open("./sec_check_yaml/security_capability.yaml")
    security_capability = yaml.load(cap, Loader= yaml.FullLoader)


    result = {'category':  'platform',
              'case_name': 'capability_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        resp = v1.create_namespaced_pod(body=security_capability, namespace='default')
        
        time.sleep(3)
        

        cmd = ['cat','/proc/1/status']
        response = kube_exec(resp, cmd)
        
        if "00000000a80435fb" in response:
            result['criteria'] = 'fail'
            status.append("CapPrm:00000000a80435fb")


        v1.delete_namespaced_pod(name=resp.metadata.name, namespace='default')

    except Exception as e:
        status.append(e)
        
    result['details'].append(status)

    store_result(result)
    return result




# privileges check 
def privilege_check():
    v1 = kube_api()
    cap = open("./sec_check_yaml/security_privileges.yaml")
    security_privileges = yaml.load(cap, Loader= yaml.FullLoader)

    result = {'category':  'platform',
              'case_name': 'privilege_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        resp = v1.create_namespaced_pod(body=security_privileges, namespace='default')

        time.sleep(5)

        cmd = ['ps', 'aux']
        
        response = kube_exec(resp, cmd)
        #print(response)

        if("root" in response):
            result['criteria'] = 'fail'
            status.append(response)

        v1.delete_namespaced_pod(name=resp.metadata.name, namespace='default')

    except Exception as e:
        status.append(e)

    result['details'].append(status)

    store_result(result)
    return result




# host network check
def host_network_check():
    v1 = kube_api()

    cap = open("./sec_check_yaml/security_host_network.yaml")
    host_network = yaml.load(cap, Loader= yaml.FullLoader)

    result = {'category':  'platform',
              'case_name': 'host_network_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        resp = v1.create_namespaced_pod(body=host_network, namespace='default')

        time.sleep(3)
   
        v1.delete_namespaced_pod(name=resp.metadata.name, namespace='default')
        result['criteria'] = 'fail'
    
    except Exception as e:
        status.append(e)
        
    result['details'].append(status)

    store_result(result)
    return result



# host directory as a volume check
def host_path_vol_check():
    v1 = kube_api()
    cap = open("./sec_check_yaml/security_host_path_vol.yaml")
    security_host_dir = yaml.load(cap, Loader= yaml.FullLoader)

    result = {'category':  'platform',
              'case_name': 'host_path_dir_vol_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        resp = v1.create_namespaced_pod(body=security_host_dir, namespace='default')

        time.sleep(3)

        v1.delete_namespaced_pod(name=resp.metadata.name, namespace='default')
        result['criteria'] = 'fail'
    
    except Exception as e:
        status.append(e)
        
    result['details'].append(status)

    store_result(result)
    return result
    


# kubernetes api connectivity check
def k8s_api_conn_check():

    result = {'category':  'platform',
              'case_name': 'connectivity_check',
              'criteria':  'pass',
              'details': []
             }

    status = []

    try:
        response = kube_curl('api')

        if ("APIVersions" in response):
            result['criteria'] = 'pass'
        else:
            result['criteria'] = 'fail'

        status.append(response)

    except Exception as e:
        status.append(e)
        
    result['details'].append(status)

    store_result(result)
    return result