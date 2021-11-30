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
Kuberef Validator
"""

import logging
from datetime import datetime as dt

from internal import store_result
from internal.validator.validator import Validator
from internal.validator.kuberef.policy_checks import topology_manager_policy_check, cpu_manager_policy_check
from internal.validator.kuberef.security_check import capability_check, privilege_check, host_network_check
from internal.validator.kuberef.security_check import host_path_vol_check, k8s_api_conn_check
from internal.validator.kuberef.monitoring_agent_checker import collectd_check, monitoring_agent_check
from internal.validator.kuberef.node_exporter_checker import node_exporter_check
from internal.validator.kuberef.plugin_check import cni_plugin_check, multi_interface_cni_check
from internal.validator.kuberef.helm_check import helmv2_disabled_check
from internal.validator.kuberef.kubevirt_health_check import kubevirt_check
from tools.conf import settings
from tools.kube_utils import load_kube_api

from . import *





class KuberefValidator(Validator):
    """Class for Kuberef Validation
    """

    def __init__(self):
        """
        Initialisation function.
        """
        super(KuberefValidator, self).__init__()
        self._logger = logging.getLogger(__name__)

        self._report = {"installer": "Kuberef",
                        "criteria": "pass",
                        "details": {"total_checks": 0,
                                    "metadata": {},
                                    "pass": [],
                                    "fail": []
                                   }
                        }

        load_kube_api()




    def validate(self):
        """
        Validation method for kuberef
        """

        self._report['scenario'] = 'none'
        self._report['start_date'] = dt.now().strftime('%Y-%m-%d %H:%M:%S')


        test_suite = settings.getValue("test_suite")


        if test_suite == "default":
            self._report['case_name'] = 'default_kuberef'
            self.default_suite()

        self._report['stop_date'] = dt.now().strftime('%Y-%m-%d %H:%M:%S')


    def default_suite(self):
        """
        Default Test Suite
        """

        # PLATFORM CHECKS
        self.update_report(pod_health_check())
        self.update_report(kubevirt_check())
        self.update_report(helmv2_disabled_check())
        self.update_report(capability_check())
        self.update_report(privilege_check())
        self.update_report(host_network_check())
        self.update_report(host_path_vol_check())
        self.update_report(k8s_api_conn_check())


        # MONITORING & LOGGING AGENT CHECKS
        self.update_report(monitoring_agent_check())
        self.update_report(collectd_check())
        self.update_report(node_exporter_check())

        # COMPUTE CHECKS
        self.update_report(cpu_manager_policy_check())
        self.update_report(topology_manager_policy_check())


        # NETWORK CHECKS
        self.update_report(cni_plugin_check())
        self.update_report(multi_interface_cni_check())



    def get_report(self):
        """
        Return final report as dict
        """
        self._report = super(KuberefValidator, self).get_report()
        store_result(self._logger, self._report)
        return self._report
