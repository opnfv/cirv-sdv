
"""
Result API
Main entry point to use results manager
"""

import logging
from .storage.storage_api import StorageApi

class ResultApi():
    """
    Result API
    Provides various storage options to use implemented as
    plugin to storage api
    """

    def __init__(self):
        """
        Initialization function
        """
        self._logger = logging.getLogger(__name__)
        self._storage_handles = []

    def register_storage(self, storage_api):
        """
        Registers ``storage_api`` as an active storage option to use.
        """
        self._logger.debug("Loading new Storage API...")
        if not isinstance(storage_api, StorageApi):
            raise TypeError("incorrect storage type, Required StorageAPI obj")

        storage_api.load_settings()
        self._storage_handles.append(storage_api)
        self._logger.info(f'{storage_api.name} api registered')

    def unregister_storage(self, storage_api):
        """
        Removes registered ``storage_api`` if exists
        """
        while storage_api in self._storage_handles:
            self._storage_handles.remove(storage_api)

    def unregister_all(self):
        """
        Removes all registered storage endpoints
        """
        for storage_api in self._storage_handles:
            self.unregister_storage(storage_api)

    def store(self, data):
        """
        Calls all active storage_api and stores ``data`` in all of them
        """
        for api in self._storage_handles:
            api.store(data)


# pylint: disable=invalid-name
result_api = ResultApi()
