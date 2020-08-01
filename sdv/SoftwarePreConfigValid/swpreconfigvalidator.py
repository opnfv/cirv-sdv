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
Abstract class for Software Prevalidations.
Implementors, please inherit from this class.
"""


class ISwPreConfigValidator():
    """ Model for a Sw Validator """
    def __init__(self):
        """ Initialization of the Interface """
        self._default_swpreconfig_validation = None

    @property
    def validation_swpreconfig_defaults(self):
        """ Default Validation values """
        return True

    def validate(self):
        """ Validate Mandatory Configurations """
        raise NotImplementedError('Please call an implementation.')
