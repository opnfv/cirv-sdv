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
Interface for Software Validators
"""

from tools.conf import settings


class Validator():
    """
    Interface for Software to Validate
    """
    def __init__(self):
        """Initialisation function.
        """

        self._report = {}


    def update_report(self, result):
        """
        Updates report with new results
        """
        case_name = result['case_name']
        criteria = result['criteria']

        self._report['details']['total_checks'] += 1
        if criteria == 'pass':
            self._report['details']['pass'].append(case_name)
        elif criteria == 'fail':
            self._report['details']['fail'].append(case_name)
            self._report['criteria'] = 'fail'


    def get_report(self):
        """
        Return final report as dict
        """
        self._report["project_name"] = settings.getValue("project_name")
        self._report["version"] = settings.getValue("project_version")
        self._report["build_tag"] = "none"

        pdf = settings.getValue('pdf_file')
        self._report["pod_name"] = pdf['management_info']['resource_pool_name']

        return self._report
