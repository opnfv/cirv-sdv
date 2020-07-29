# Copyright 2020 Intel Corporation, Spirent Communications.
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

from conf import settings
from core.loader.loader_servant import LoaderServant
from SoftwarePreValid.swprevalidator import ISwPreValidator
from SoftwarePostValid.swpostvalidator import ISwPostValidator
from NwLinksValid.nwlinksvalidator import INwLinksValidator


# pylint: disable=too-many-public-methods
class Loader():
    """Loader class - main object context holder.
    """
    _swvalidator_loader = None

    def __init__(self):
        """Loader ctor - initialization method.

        All data is read from configuration each time Loader instance is
        created. It is up to creator to maintain object life cycle if this
        behavior is unwanted.
        """
        self._swprevalidator_loader = LoaderServant(
            settings.getValue('SW_PRE_VALID_DIR'),
            settings.getValue('SW_PRE_VALIDATOR'),
            ISwPreValidator)
        self._swpostvalidator_loader = LoaderServant(
            settings.getValue('SW_POST_VALID_DIR'),
            settings.getValue('SW_POST_VALIDATOR'),
            ISwPostValidator)
        self._nwlinksvalidator_loader = LoaderServant(
            settings.getValue('NW_LINKS_VALID_DIR'),
            settings.getValue('NW_LINKS_VALIDATOR'),
            INwLinksValidator)

    def get_swprevalidator(self):
        """ Returns a new instance configured Software Validator
        :return: ISwPreValidator implementation if available, None otherwise
        """
        return self._swprevalidator_loader.get_class()()

    def get_swprevalidator_class(self):
        """Returns type of currently configured Software Validator.

        :return: Type of ISwPreValidator implementation if available.
            None otherwise.
        """
        return self._swprevalidator_loader.get_class()

    def get_swprevalidators(self):
        """
        Get Prevalidators
        """
        return self._swprevalidator_loader.get_classes()

    def get_swprevalidators_printable(self):
        """
        Get Prevalidators for printing
        """
        return self._swprevalidator_loader.get_classes_printable()

    def get_swpostvalidator(self):
        """ Returns a new instance configured Software Validator
        :return: ISwPostValidator implementation if available, None otherwise
        """
        return self._swpostvalidator_loader.get_class()()

    def get_swpostvalidator_class(self):
        """Returns type of currently configured Software Validator.

        :return: Type of ISwPostValidator implementation if available.
            None otherwise.
        """
        return self._swpostvalidator_loader.get_class()

    def get_swpostvalidators(self):
        """
        Get Postvalidators
        """
        return self._swpostvalidator_loader.get_classes()

    def get_swpostvalidators_printable(self):
        """
        Get Postvalidators for printing
        """
        return self._swpostvalidator_loader.get_classes_printable()

    def get_nwlinksvalidator(self):
        """ Returns a new instance configured Nw-Links Validator
        :return: INwLinksValidator implementation if available, None otherwise
        """
        return self._nwlinksvalidator_loader.get_class()()

    def get_nwlinksvalidator_class(self):
        """Returns type of currently configured Nw-Links Validator.

        :return: Type of NwLinksValidator implementation if available.
            None otherwise.
        """
        return self._nwlinksvalidator_loader.get_class()

    def get_nwlinkvalidators(self):
        """
        Get Linkvalidators
        """
        return self._nwlinksvalidator_loader.get_classes()

    def get_nwlinkvalidators_printable(self):
        """
        Get Linkvalidators for printing
        """
        return self._nwlinksvalidator_loader.get_classes_printable()
