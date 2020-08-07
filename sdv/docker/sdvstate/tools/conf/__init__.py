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




"""Settings and configuration handlers.

Settings will be loaded from several .yaml or .yml files
and any user provided settings file.
"""

import os
import ast

import yaml

# pylint: disable=invalid-name

class Settings():
    """Holding class for settings.
    """
    def __init__(self):
        pass


    def getValue(self, attr):
        """
        Return a settings item value
        """
        try:
            attr = attr.lower()
            return getattr(self, attr)
        except AttributeError:
            raise AttributeError("{obj} object has no attribute \
                                 {attr}".format(obj=self.__class__, attr=attr))


    def setValue(self, name, value):
        """Set a value
        """
        if name is not None and value is not None:
            super(Settings, self).__setattr__(name.lower(), value)


    def load_from_file(self, path):
        """Update ``settings`` with values found in module at ``path``.
        """
        with open(path) as file:
            configs = yaml.load_all(file, Loader=yaml.SafeLoader)
            for conf in configs:
                for name, value in conf.items():
                    self.setValue(name, value)


    def load_from_env(self):
        """
        Update ``settings`` with values found in the environment.
        """
        for key in os.environ:
            value = os.environ[key]

            #evaluate string to python type
            try:
                value = ast.literal_eval(os.environ[key])
            except (ValueError, SyntaxError):
                pass #already string

            self.setValue(key, value)


    def load_from_dir(self, dir_path):
        """Update ``settings`` with contents of the yaml files at ``path``.

        Files are read in ascending order, hence if a configuration item
        exists in more than one file, then the setting in the file that
        occurs in the last read file will have high precedence and
        overwrite previous values.

        Same precedence logic for sub-directories.
        Also, child directory will have more precedence than it's parent

        :param dir_path: The full path to the dir from which to load the
             yaml files.

        :returns: None
        """
        files = list_yamls(dir_path)

        for file in files:
            self.load_from_file(file)


settings = Settings()


def list_yamls(dir_path):
    """Get all yaml files recursively in ``dir_path``
    """
    files = []
    dir_list = [x[0] for x in os.walk(dir_path)]
    dir_list.sort()
    for path in dir_list:
        dir_files = [path+'/'+f for f in os.listdir(path)
                     if f.endswith('.yaml') or f.endswith('.yml')]
        if dir_files is not None:
            dir_files.sort()
        files.extend(dir_files)
    return files
