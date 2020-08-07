
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
