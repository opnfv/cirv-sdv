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


"""Loads PDF file into settings
"""

import json
import os
import requests
import yaml

from tools.conf import settings

def load_pdf():
    """
    Updates settings with PDF data
    """
    path = settings.getValue('pdf_file')
    data = ""
    if os.path.exists(path):
        with open(path) as handle:
            data = handle.read()
    else:
        if path.find("github.com") != -1:
            path = path.replace("github.com", "raw.githubusercontent.com")
            path = path.replace("/blob", "")
            if path[:8] != "https://":
                path = "https://" + path
        try:
            resp = requests.get(path)
            if resp.status_code == requests.codes.ok:
                data = resp.text
        except:
            raise Exception(f"Invalid path: {path}")

    try:
        pdf = json.loads(data)
    except json.decoder.JSONDecodeError:
        try:
            pdf = yaml.safe_load(data)
        except yaml.parser.ParserError:
            raise Exception(f"Invalid PDF file: {path}")

    settings.setValue('pdf_file', pdf)
