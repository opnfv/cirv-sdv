# Copyright 2020 Spirent Communications.
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
Abstract class for N/W Lnks Prevalidations.
Implementors, please inherit from this class.
"""


class INwLinksValidator():
    """ Model for a Links Validator """
    def __init__(self):
        """ Initialization of the Interface """
        self._default_nwlinks_validation = None

    @property
    def validation_nwlinks_defaults(self):
        """ Default Validation values """
        return True

    def validate_compute_node_links(self):
        """ Validating Compute Node Links"""
        raise NotImplementedError('Please call an implementation.')

    def validate_control_node_links(self):
        """ Validating Controller Node Links"""
        raise NotImplementedError('Please call an implementation.')
