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
from SoftwarePreUrlsValid.swpreurlsvalidator import ISwPreUrlsValidator
from SoftwarePreConfigValid.swpreconfigvalidator import ISwPreConfigValidator
from SoftwarePostStateValid.swpoststatevalidator import ISwPostStateValidator
from SoftwarePostSecurityValid.swpostsecurityvalidator import ISwPostSecurityValidator
from NwLinksValid.nwlinksvalidator import INwLinksValidator
from ResourceModelValid.resmodvalidator import IResModValidator


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
        self._swpreurlsvalidator_loader = LoaderServant(
            settings.getValue('SW_PRE_URLS_VALID_DIR'),
            settings.getValue('SW_PRE_URLS_VALIDATOR'),
            ISwPreUrlsValidator)
        self._swpreconfigvalidator_loader = LoaderServant(
            settings.getValue('SW_PRE_CONFIG_VALID_DIR'),
            settings.getValue('SW_PRE_CONFIG_VALIDATOR'),
            ISwPreConfigValidator)
        self._swpoststatevalidator_loader = LoaderServant(
            settings.getValue('SW_POST_STATE_VALID_DIR'),
            settings.getValue('SW_POST_STATE_VALIDATOR'),
            ISwPostStateValidator)
        self._swpostsecurityvalidator_loader = LoaderServant(
            settings.getValue('SW_POST_SECURITY_VALID_DIR'),
            settings.getValue('SW_POST_SECURITY_VALIDATOR'),
            ISwPostSecurityValidator)
        self._nwlinksvalidator_loader = LoaderServant(
            settings.getValue('NW_LINKS_VALID_DIR'),
            settings.getValue('NW_LINKS_VALIDATOR'),
            INwLinksValidator)
        self._resmodvalidator_loader = LoaderServant(
            settings.getValue('RES_MOD_VALID_DIR'),
            settings.getValue('RES_MOD_VALIDATOR'),
            IResModValidator)

    def get_swpreurlsvalidator(self):
        """ Returns a new instance configured Software Validator
        :return: ISwPreUrlsValidator implementation if available, None otherwise
        """
        return self._swpreurlsvalidator_loader.get_class()()

    def get_swpreurlsvalidator_class(self):
        """Returns type of currently configured Software Validator.

        :return: Type of ISwPreUrlsValidator implementation if available.
            None otherwise.
        """
        return self._swpreurlsvalidator_loader.get_class()

    def get_swpreurlsvalidators(self):
        """
        Get Prevalidators
        """
        return self._swpreurlsvalidator_loader.get_classes()

    def get_swpreurlsvalidators_printable(self):
        """
        Get Prevalidators for printing
        """
        return self._swpreurlsvalidator_loader.get_classes_printable()

    def get_swpreconfigvalidator(self):
        """ Returns a new instance configured Software Validator
        :return: ISwPreConfigValidator implementation if available, None otherwise
        """
        return self._swpreconfigvalidator_loader.get_class()()

    def get_swpreconfigvalidator_class(self):
        """Returns type of currently configured Software Validator.

        :return: Type of ISwPreConfigValidator implementation if available.
            None otherwise.
        """
        return self._swpreconfigvalidator_loader.get_class()

    def get_swpreconfigvalidators(self):
        """
        Get Prevalidators
        """
        return self._swpreconfigvalidator_loader.get_classes()

    def get_swpreconfigvalidators_printable(self):
        """
        Get Prevalidators for printing
        """
        return self._swpreconfigvalidator_loader.get_classes_printable()

    def get_swpoststatevalidator(self):
        """ Returns a new instance configured Software Validator
        :return: ISwPostStateValidator implementation if available, None otherwise
        """
        return self._swpoststatevalidator_loader.get_class()()

    def get_swpoststatevalidator_class(self):
        """Returns type of currently configured Software Validator.

        :return: Type of ISwPostStateValidator implementation if available.
            None otherwise.
        """
        return self._swpoststatevalidator_loader.get_class()

    def get_swpoststatevalidators(self):
        """
        Get Postvalidators
        """
        return self._swpoststatevalidator_loader.get_classes()

    def get_swpoststatevalidators_printable(self):
        """
        Get Postvalidators for printing
        """
        return self._swpoststatevalidator_loader.get_classes_printable()

    def get_swpostsecurityvalidator(self):
        """ Returns a new instance configured Software Validator
        :return: ISwPostSecurityValidator implementation if available, None otherwise
        """
        return self._swpostsecurityvalidator_loader.get_class()()

    def get_swpostsecurityvalidator_class(self):
        """Returns type of currently configured Software Validator.

        :return: Type of ISwPostSecurityValidator implementation if available.
            None otherwise.
        """
        return self._swpostsecurityvalidator_loader.get_class()

    def get_swpostsecurityvalidators(self):
        """
        Get Postvalidators
        """
        return self._swpostsecurityvalidator_loader.get_classes()

    def get_swpostsecurityvalidators_printable(self):
        """
        Get Postvalidators for printing
        """
        return self._swpostsecurityvalidator_loader.get_classes_printable()

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

    def get_nwlinksvalidators(self):
        """
        Get Linkvalidators
        """
        return self._nwlinksvalidator_loader.get_classes()

    def get_nwlinksvalidators_printable(self):
        """
        Get Linkvalidators for printing
        """
        return self._nwlinksvalidator_loader.get_classes_printable()

    def get_resmodvalidator(self):
        """ Returns a new instance configured Nw-Links Validator
        :return: IResModValidator implementation if available, None otherwise
        """
        return self._resmodvalidator_loader.get_class()()

    def get_resmodvalidator_class(self):
        """Returns type of currently configured Nw-Links Validator.

        :return: Type of ResModValidator implementation if available.
            None otherwise.
        """
        return self._resmodvalidator_loader.get_class()

    def get_resmodvalidators(self):
        """
        Get ResoureModelValidators
        """
        return self._resmodvalidator_loader.get_classes()

    def get_resmodvalidators_printable(self):
        """
        Get ResoureModelValidators for printing
        """
        return self._resmodvalidator_loader.get_classes_printable()
