
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
