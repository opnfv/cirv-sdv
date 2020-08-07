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
import ast
import json

from tools.conf import settings
from tools.result_api import result_api, rfile
from tools.kube_utils import *
from validator.validator import Validator

## Checks
from .pod_health_check import pod_health_check



class AirshipValidator(Validator):
    """Class for Airship Validation
    """

    def __init__(self):
        """
        Initialisation function.
        """
        super(AirshipValidator, self).__init__()
        self._logger = logging.getLogger(__name__)

        load_kube_api()
  

    def validate(self):
        """
        """
        pod_health_check()
