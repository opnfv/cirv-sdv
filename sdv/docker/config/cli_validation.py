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

# pylint: disable=too-many-instance-attributes, too-many-arguments

""" validation code """

import os
import json
import logging
import argparse
import sys
import datetime
from manifest import Manifest
from validation import HardwareValidation, InfoValidation, PlatformValidation
from validation import SoftwareValidation, NetworkValidation, StorageValidation
from testapi import PushResults

CWD = os.getcwd()


class Validate():
    """ Validation class """

    def __init__(self, yaml_dir, mapping_file_type, json_fn, global_sw_dir, type_sw_dir):
        # initialize internal values
        self.correct = 0
        self.wrong = 0
        self.total = 0
        self.json = dict()
        self.testapi_result = dict()
        self.logger = ""
        self.result = ""
        # store external values
        self.global_sw_dir = global_sw_dir
        self.site_sw_dir = os.path.join(yaml_dir, 'software')
        self.type_sw_dir = type_sw_dir

        self.start_logger()
        self.read_json(json_fn)
        self.manifest = Manifest(
            inst_dir=yaml_dir,
            mapping_file_dir=os.path.join(
                "mapping/",
                mapping_file_type),
            logger=self.logger)

    def read_json(self, json_fn):
        """ read json file """
        try:
            with open(os.path.join(CWD, json_fn)) as json_file:
                self.json = json.loads(json_file.read())
        except IOError:
            self.logger.critical("Unable to read the pdf file:%s", json_fn)
            self.logger.info("Exiting process")
            sys.exit()

    def start_logger(self):
        """ starting logging process """
        logging.basicConfig(filename='validation.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        self.logger = logging.getLogger('validation')
        self.logger.info("Starting validation program")

    def validate(self):
        """ description about validation """
        # validate info
        correct, wrong, total, result = InfoValidation(
            self.json, self.manifest, self.logger).get_values()
        self.correct += correct
        self.wrong += wrong
        self.total += total
        string = (
            "The number of correct :{} wrong:{} and total:{} in info profile\n\n".format(
                self.correct,
                self.wrong,
                self.total))
        self.result += result + string

        # iterate through the roles: have a class for each for each of the roles
        for _, value in enumerate(self.json["roles"]):
            role = value["name"]
            # print(role,value["hardware_profile"])
            correct, wrong, total, result = HardwareValidation(
                self.json, value["hardware_profile"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = (
                "The number of correct :{} wrong:{} and total:{} in hardware profile\n\n".format(
                    correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = StorageValidation(
                role, self.json, value["storage_mapping"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = (
                "The number of correct :{} wrong:{} and total:{} in storage profile\n\n".format(
                    correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = SoftwareValidation(role, self.json, \
                value["sw_set_name"], self.manifest, self.global_sw_dir, self.type_sw_dir, \
                    self.site_sw_dir, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = (
                "The number of correct :{} wrong:{} and total:{} in software profile\n\n".format(
                    correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = PlatformValidation(
                role, self.json, value["platform_profile"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = (
                "The number of correct :{} wrong:{} and total:{} in platform profile\n\n".format(
                    correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = NetworkValidation(role, self.json, \
                value["interface_mapping"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = (
                "The number of correct :{} wrong:{} and total:{} in network profile\n\n".format(
                    correct, wrong, total))
            self.result += result + string

        self.testapi_result["timestamp"] = datetime.datetime.now()
        self.testapi_result["correct"] = self.correct
        self.testapi_result["wrong"] = self.wrong
        self.testapi_result["total"] = self.total

        # print the final report
        self.logger.info("Validation complete!")
        # push results to opnfv testapi
        PushResults(self.testapi_result, self.logger)

        return self.result


if __name__ == "__main__":
    # Initiate the parser
    PARSER = argparse.ArgumentParser(description="validation program")

    # Add long and short argument for test
    # parser.add_argument("--test", help="test the code", action="store_true")

    # Add long and short argument for manifest dir
    PARSER.add_argument("--inst_dir", help="get installer dir")

    # Add long and short argument for mapping dir
    PARSER.add_argument("--inst_type", help="get installer type")

    # Add long and short argument for pdf file
    PARSER.add_argument("--pdf", help="get pdf")

    # Add long and short argument for pdf file
    PARSER.add_argument("--gsw", help="get global software dir")

    # Add long and short argument for pdf file
    PARSER.add_argument("--tsw", help="type software dir")

    # Read arguments from the command line
    ARGS = PARSER.parse_args()

    print(Validate(ARGS.inst_dir, ARGS.inst_type, ARGS.pdf, ARGS.gsw, ARGS.tsw).validate())
