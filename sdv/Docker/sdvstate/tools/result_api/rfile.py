

"""rfile is Object representation of a file for Result_api and storage_api
"""

import logging

# pylint: disable=invalid-name

class rfile():
    """
    rfile object to represent files in Result API
    """

    def __init__(self, data):
        """
        Initialisation function
        """
        self._logger = logging.getLogger(__name__)
        self.hold_data(data)

    def get_data(self):
        """
        Returns stored data
        """
        if self._data == '':
            self._logger.warning('Reading from a empty \'rfile\'')
        return self._data


    def hold_data(self, data):
        """
        Holds data of a file
        """
        if data is None:
            self._logger.warning('Storing an empty \'rfile\'')
            data = ''
        self._data = data
