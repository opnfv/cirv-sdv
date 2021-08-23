import logging
from tools.kube_utils import kube_api
from tools.conf import settings
from tools.result_api import rfile
import ast, json
from .store_result import store_result
import subprocess as sp 

def helm_v2_check():
    result = {'category':  'network',
              'case_name': 'helmv2_disabled_check',
              'criteria':  'pass',
              'details': []
             }
    o = sp.getoutput('kubectl get secrets')
    if('helm.sh/version.v1' not in o):
        result['criteria'] = 'fail'
    
    result['details'].append(o)
    store_result(result)
    return result