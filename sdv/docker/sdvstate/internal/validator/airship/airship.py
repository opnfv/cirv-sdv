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
Airship Validator
"""

import logging
from datetime import datetime as dt

from tools.conf import settings
from tools.kube_utils import load_kube_api, delete_kube_curl_pod
from internal.validator.validator import Validator
from internal import store_result

from . import *





class AirshipValidator(Validator):
    """Class for Airship Validation
    """

    def __init__(self):
        """
        Initialisation function.
        """
        super(AirshipValidator, self).__init__()
        self._logger = logging.getLogger(__name__)

        self._report = {"installer": "Airship",
                        "criteria": "pass",
                        "details": {"total_checks": 0,
                                    "pass": [],
                                    "fail": [],
                                    "metadata": {}
                                   }
                        }

        load_kube_api()


    def validate(self):
        """
        Validation method
        """

        self._report['scenario'] = 'none'
        self._report['start_date'] = dt.now().strftime('%Y-%m-%d %H:%M:%S')

        test_suite = settings.getValue("test_suite")

        if test_suite == "default":
            self._report['case_name'] = 'ook_airship'
            self.default_suite()

        delete_kube_curl_pod()

        self._report['stop_date'] = dt.now().strftime('%Y-%m-%d %H:%M:%S')


    def default_suite(self):
        """
        Default Test Suite
        """

        # PLATFORM CHECKS
        self.update_report(pod_health_check())
        self.update_report(readiness_probe_check())
        self.update_report(liveness_probe_check())
        self.update_report(startup_probe_check())

        # STORAGE CHECKS
        self.update_report(ceph_health_check())

        # MONITORING & LOGGING AGENTS CHECKS
        self.update_report(prometheus_check())
        self.update_report(grafana_check())
        ## current version of AlertManager doesn't support this
        # prometheus_alert_manager_check()
        self.update_report(elasticsearch_check())
        self.update_report(kibana_check())
        self.update_report(nagios_check())
        self.update_report(elasticsearch_exporter_check())
        self.update_report(fluentd_exporter_check())

        # NETWORK CHECKS
        self.update_report(physical_network_check())

        # COMPUTE CHECKS
        self.update_report(reserved_vnf_cores_check())
        self.update_report(isolated_cores_check())
        self.update_report(vswitch_pmd_cores_check())
        self.update_report(vswitch_dpdk_lcores_check())
        self.update_report(os_reserved_cores_check())
        self.update_report(nova_scheduler_filters_check())
        self.update_report(cpu_allocation_ratio_check())


    def get_report(self):
        """
        Return final report as dict
        """
        self._report = super(AirshipValidator, self).get_report()
        store_result(self._logger, self._report)
        return self._report
