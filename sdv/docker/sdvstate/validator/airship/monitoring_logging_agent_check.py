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
Monitoring & Logging Agents Related Checks
"""

import ast

from tools.kube_utils import kube_curl
from tools.result_api import rfile
from .store_result import store_result


def prometheus_check():
    """
    Check health of Prometheus
    """
    username = "prometheus"
    password = "password123"
    service = "prom-metrics"
    namespace = "osh-infra"

    health = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-u", f'{username}:{password}', f'{service}.{namespace}/-/healthy')
    if 'Prometheus is Healthy' in res:
        health = "pass"

    readiness = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-u", f'{username}:{password}', f'{service}.{namespace}/-/ready')
    if 'Prometheus is Ready' in res:
        readiness = "pass"

    if health == "pass" and readiness == "pass":
        state = "pass"
    else:
        state = "fail"

    result = {'category':  'platform',
              'case_name': 'prometheus_check',
              'criteria':  state,
              'details': {'health': health, 'readiness': readiness}
             }

    store_result(result)
    return result



def grafana_check():
    """
    Check health of Grafana
    """
    username = "grafana"
    password = "password123"
    service = "grafana-dashboard"
    namespace = "osh-infra"

    state = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-w", "%{http_code}",\
                    "-o", "/dev/null", "-u",  \
                    f'{username}:{password}', \
                    f'{service}.{namespace}:3000/api/health')
    if res == '200':
        state = "pass"

    result = {'category':  'platform',
              'case_name': 'grafana_check',
              'criteria':  state
             }

    store_result(result)
    return result


def prometheus_alert_manager_check():
    """
    Check health of Alert Manager
    """
    service = "alerts-engine"
    namespace = "osh-infra"

    health = "fail" #default
    res = kube_curl("-sL", "-m", "3", f'{service}.{namespace}:9093/-/healthy')
    if 'Prometheus is Healthy' in res:
        health = "pass"

    readiness = "fail" #default
    res = kube_curl("-sL", "-m", "3", f'{service}.{namespace}:9093/-/ready')
    if 'Prometheus is Ready' in res:
        readiness = "pass"

    if health == "pass" and readiness == "pass":
        state = "pass"
    else:
        state = "fail"

    result = {'category':  'platform',
              'case_name': 'prometheus_alert_manager_check',
              'criteria':  state,
              'details': {'health': health, 'readiness': readiness}
             }


    store_result(result)
    return result


def elasticsearch_check():
    """
    Check health of Elasticsearch cluster
    """
    username = "elasticsearch"
    password = "password123"
    service = "elasticsearch"
    namespace = "osh-infra"

    state = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-u", f'{username}:{password}', f'{service}.{namespace}/_cluster/health')

    if res == '':
        res = 'Elasticsearch not reachable'
    else:
        res = ast.literal_eval(res)
        if res['status'] == 'green':
            state = "pass"

    result = {'category':  'platform',
              'case_name': 'elasticsearch_check',
              'criteria':  state,
              'details': res
             }

    store_result(result)
    return result


def kibana_check():
    """
    Check health of Kibana
    """
    username = "elasticsearch"
    password = "password123"
    service = "kibana-dash"
    namespace = "osh-infra"

    state = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-u", f'{username}:{password}', f'{service}.{namespace}/api/status')

    if res == '':
        res = 'kibana not reachable'
    else:
        res = ast.literal_eval(res)
        if res['status']['overall']['state'] == 'green':
            state = "pass"

    result = {'category':  'platform',
              'case_name': 'kibana_check',
              'criteria':  state,
              'details': rfile(str(res))
             }

    store_result(result)
    return result


def nagios_check():
    """
    Check health of Nagios
    """
    username = "nagios"
    password = "password123"
    service = "nagios-metrics"
    namespace = "osh-infra"

    state = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-w", "%{http_code}",\
                    "-o", "/dev/null", "-u",  \
                    f'{username}:{password}', \
                    f'{service}.{namespace}')
    if res == '200':
        state = "pass"

    result = {'category':  'platform',
              'case_name': 'nagios_check',
              'criteria':  state
             }

    store_result(result)
    return result


def elasticsearch_exporter_check():
    """
    Check health of Elasticsearch Exporter
    """
    service = "elasticsearch-exporter"
    namespace = "osh-infra"

    state = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-w", "%{http_code}", "-o", "/dev/null", f'{service}.{namespace}:9108/metrics')
    if res == '200':
        state = "pass"

    result = {'category':  'platform',
              'case_name': 'elasticsearch_exporter_check',
              'criteria':  state
             }

    store_result(result)
    return result


def fluentd_exporter_check():
    """
    Check health of Fluentd Exporter
    """
    service = "fluentd-exporter"
    namespace = "osh-infra"

    state = "fail" #default
    res = kube_curl("-sL", "-m", "3", "-w", "%{http_code}", "-o", "/dev/null", f'{service}.{namespace}:9309/metrics')
    if res == '200':
        state = "pass"

    result = {'category':  'platform',
              'case_name': 'fluentd_exporter_check',
              'criteria':  state
             }

    store_result(result)
    return result
