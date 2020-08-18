#!/usr/bin/env python

# Copyright (C) 2020 Ashwin Nayak
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

""" testapi class to push results to opnfv testapi """

from datetime import datetime as dt
import requests

OPNFV_URL = "http://testresults.opnfv.org/test/api/v1"
POD_NAME = 'intel-pod10'
INSTALLER = 'Airship'
BUILD_TAG = "none"
PKG_LIST = 'package-list.mk'
START_TIME = dt.now().strftime('%Y-%m-%d %H:%M:%S')
STOP_TIME = dt.now().strftime('%Y-%m-%d %H:%M:%S')
TC_NAME = 'SDV_config_basic'
VERSION = '1.0'
CRITERIA = 'PASS'


class PushResults():
    """ Push results to opnfv test api """

    def __init__(self, results, logger):
        """ constructor """
        # store external values
        self.results = results
        self.logger = logger
        # initialize internal values
        self.push_vals = dict()
        # call functions
        self.generate_response()
        self.push_results()

    def generate_response(self):
        """ generate json output to be pushed """
        # Build body
        body = {
            "project_name": "sdv",
            "scenario": "none",
            "start_date": START_TIME,
            "stop_date": STOP_TIME,
            "case_name": TC_NAME,
            "pod_name": POD_NAME,
            "installer": INSTALLER,
            "version": VERSION,
            "build_tag": BUILD_TAG,
            "criteria": CRITERIA,
            "details": self.results
        }
        self.logger.debug("The generated json response to be pushed:%s", body)
        # store this value in the class variable
        self.push_vals = body

    def push_results(self):
        """ push results to testapi """
        url = OPNFV_URL + "/results"

        try:
            response = requests.post(url, json=self.push_vals)
            self.logger.info("testapi push response:%s", response)
        except ConnectionError:
            self.logger.exception("error while pushing results to testapi")
            self.logger.error("failed to push results")
