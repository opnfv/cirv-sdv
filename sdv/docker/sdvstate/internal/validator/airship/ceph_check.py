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
Ceph Related Checks
"""

import ast
import logging

from tools.kube_utils import get_pod_with_labels, kube_exec
from internal import store_result




def ceph_health_check():
    """
    Check health of Ceph
    """
    logger = logging.getLogger(__name__)
    pod = get_pod_with_labels('application=ceph,component=mon')

    cmd = ['ceph', 'health', '-f', 'json']
    response = kube_exec(pod, cmd)

    response = ast.literal_eval(response)

    result = {'category':  'storage',
              'case_name': 'ceph_health_check',
              'details': []
             }

    if response['status'] == 'HEALTH_OK':
        result['criteria'] = 'pass'
        result['details'] = 'HEALTH_OK'
    else:
        result['criteria'] = 'fail'
        result['details'] = response

    store_result(logger, result)
    return result
