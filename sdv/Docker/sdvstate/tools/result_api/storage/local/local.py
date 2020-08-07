
"""
Local Storage Api
"""

import logging
import os
import random
import string
import json
from tools.conf import settings

from ..storage_api import StorageApi
from ... import rfile

# pylint: disable=invalid-name

class Local(StorageApi):
    """
    Storage API
    Provides abstract class for various storage options to implement as
    plugin to storage api
    """

    def __init__(self):
        """
        Initialization function
        """
        super(Local, self).__init__()
        self.name = 'Local Storage'
        self._logger = logging.getLogger(__name__)

    def store(self, data):
        """
        stores ``data``, ``data`` should be a dict
        """
        if not isinstance(data, dict):
            raise TypeError("incorrect data type to store, dict required")

        if not os.path.isfile(self._filename):
            with open(self._filename, 'w') as f:
                json.dump([], f)

        with open(self._filename, 'r') as f:
            records = json.load(f)
            temp_data = data.copy()
            eval_rfile(temp_data)
            records.append(temp_data)

        with open(self._filename, 'w') as f:
            self._logger.info(f'{self.name}: New record saved')
            json.dump(records, f, indent=4, sort_keys=True, default=str)


    def load_settings(self):
        """
        Load all required settings otherwise set to default
        Settings to load:
        * ``result_path`` (default: /tmp/local/)
        * ``results_filename`` (default: results.json)
        """
        try:
            path = settings.getValue('results_path')
        except AttributeError:
            path = '/tmp/local/'
            settings.setValue('results_path', path)

        try:
            filename = settings.getValue('results_filename')
        except AttributeError:
            filename = 'results.json'
            settings.setValue('results_filename', filename)

        if not os.path.exists(path):
            os.makedirs(path)

        self._path = path
        self._filename = path + filename





def eval_rfile(data):
    """
    Find all values of a type rfile in data dict/list and evals them into
    actual file
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, rfile):
                data[key] = rfile_save(value, key)
            else:
                eval_rfile(value)
    if isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], rfile):
                data[i] = rfile_save(data[i])
            else:
                eval_rfile(data[i])


def rfile_save(rfile_obj, prefix='zz'):
    """
    Takes rfile Object and stores it into random file returning filename
    """
    letters = string.ascii_lowercase
    suffix = ''.join(random.choice(letters) for i in range(6))
    filename = settings.getValue('results_path') + f'{prefix}-{suffix}.txt'
    if os.path.isfile(filename):
        return rfile_save(rfile_obj, prefix)
    else:
        with open(filename, 'w') as rf:
            rf.write(rfile_obj.get_data())
        return f'{prefix}-{suffix}.txt'
