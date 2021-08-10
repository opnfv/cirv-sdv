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

        # COMPUTE CHECKS


    def get_report(self):
        """
        Return final report as dict
        """
        self._report = super(KuberefValidator, self).get_report()
        store_result(self._logger, self._report)
        return self._report
