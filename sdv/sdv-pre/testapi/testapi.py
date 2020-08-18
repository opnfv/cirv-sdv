#!/usr/bin/env python

# Copyright (C) 2020 Ashwin Nayak <ashwinnayak111@gmail.com>

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# pylint: disable=line-too-long, invalid-name, broad-except, too-many-instance-attributes, too-many-arguments

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
VERSION='1.0'
CRITERIA='PASS'

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
        except Exception:
            self.logger.exception("error while pushing results to testapi")
            self.logger.error("failed to push results")