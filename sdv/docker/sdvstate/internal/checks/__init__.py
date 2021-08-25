
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
Package for platform agnosit check functions

This package holds common validation logic for
various checks implemented in sdv framework. The functions
defined in this package are agnostic to target cloud plaform.

The functions are also agnostic to cloud platform specific settings
variables.
"""


### Pod Health Checks
from .pod_health_check import pod_health_check
