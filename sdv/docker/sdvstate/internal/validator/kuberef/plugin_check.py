import logging
from tools.kube_utils import kube_api, kube_curl
from tools.conf import settings
from tools.result_api import rfile
import ast, json
from .store_result import store_result
import subprocess as sp 
import re

def cni_plugin_check():
    cni_plugins = settings.getValue('pdf_file')['undercloud_ook']['cni_plugins']
    cmd = """ssh opnfv@10.10.180.21 'ls /opt/cni/bin'"""                                                               
    out = sp.getoutput(cmd)
    result = {'category':  'network',
              'case_name': 'cni_plugin_check',
              'criteria':  'pass',
              'details': []
             }
    if cni_plugins != out:
        result['criteria'] = 'fail'
    result['details'].append(out)

    store_result(result)
    return result

def device_plugin_check():
    device_plugins = settings.getValue('pdf_file')['undercloud_ook']['device_plugins']
    resp = kube_curl("")
    dp = []
    result = {'category':  'network',
              'case_name': 'device_plugin_check',
              'criteria':  'pass',
              'details': []
             }
    for line in resp:
        if re.search("device-plugin", line):
            dp.append(line)
    
    for i in device_plugins:
        if i not in dp:
            result['criteria'] = 'fail'
            break
    
    result['details'].append(dp)
    store_result(result)
    return result
