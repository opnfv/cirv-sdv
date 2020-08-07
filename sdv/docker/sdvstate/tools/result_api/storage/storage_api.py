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
Abstract class for Storage API
"""

import logging


class StorageApi():
    """
    Storage API
    Provides abstract class for various storage options to implement as
    plugin to storage api
    """

    def __init__(self):
        """
        Initialization function
        """
        self._logger = logging.getLogger(__name__)

    def store(self, data):
        """
        stores ``data``
        """
        raise NotImplementedError()

    def load_settings(self):
        """
        Load all required settings
        """
        raise NotImplementedError()
