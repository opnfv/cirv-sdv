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

# pylint: disable=line-too-long, invalid-name, missing-module-docstring

""" validation code """

import os
import json
import logging
import argparse
import sys
import datetime
from manifest import Manifest
from validation import HardwareValidation, InfoValidation, PlatformValidation, SoftwareValidation, NetworkValidation, StorageValidation
from testapi import PushResults

CWD = os.getcwd()

class Validate():
    """ Validation class """
    def __init__(self, yaml_dir, mapping_file_type, json_fn, global_sw_dir, type_sw_dir):
        self.correct = 0
        self.wrong = 0
        self.total = 0
        self.json = dict()
        self.logger = ""
        self.result = ""
        self.global_sw_dir = global_sw_dir
        self.site_sw_dir = os.path.join(yaml_dir, 'software')
        self.type_sw_dir = type_sw_dir

        self.start_logger()
        self.read_json(json_fn)
        self.manifest = Manifest(inst_dir=yaml_dir, mapping_file_dir=os.path.join("/sdv-pre/mapping/", mapping_file_type), logger=self.logger)

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
        correct, wrong, total, result = InfoValidation('masters', self.json, self.manifest, self.logger).get_values()
        self.correct += correct
        self.wrong += wrong
        self.total += total
        string = ("The number of correct :{} wrong:{} and total:{} in info profile\n\n".format(self.correct, self.wrong, self.total))
        self.result += result + string

        # iterate through the roles: have a class for each for each of the roles
        for _, value in enumerate(self.json["roles"]):
            role = value["name"]
            # print(role,value["hardware_profile"])
            correct, wrong, total, result = HardwareValidation(role, self.json, value["hardware_profile"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in hardware profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = StorageValidation(role, self.json, value["storage_mapping"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in storage profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = SoftwareValidation(role, self.json, value["sw_set_name"], self.manifest, self.global_sw_dir, self.type_sw_dir, self.site_sw_dir, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in software profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = PlatformValidation(role, self.json, value["platform_profile"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in platform profile\n\n".format(correct, wrong, total))
            self.result += result + string

            correct, wrong, total, result = NetworkValidation(role, self.json, value["interface_mapping"], self.manifest, self.logger).get_values()
            self.correct += correct
            self.wrong += wrong
            self.total += total
            string = ("The number of correct :{} wrong:{} and total:{} in network profile\n\n".format(correct, wrong, total))
            self.result += result + string

        self.result += "Timestamp:{}\n".format(datetime.datetime.now())
        self.result += "correct:{} wrong:{} total:{}\n".format(self.correct, self.wrong, self.total)
        self.result += "percentage of correct:{:.2f} wrong:{:.2f}\n".format(self.correct / (self.correct + self.wrong), self.wrong / (self.correct + self.wrong))
        # print the final report
        self.logger.info("Validation complete!")
        # push results to opnfv testapi
        PushResults(self.result, self.logger)

        return self.result

if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser(description="validation program")

    # Add long and short argument for test
    # parser.add_argument("--test", help="test the code", action="store_true")

    # Add long and short argument for manifest dir
    parser.add_argument("--inst_dir", help="get installer dir")

    # Add long and short argument for mapping dir
    parser.add_argument("--inst_type", help="get installer type")

    # Add long and short argument for pdf file
    parser.add_argument("--pdf", help="get pdf")

    # Add long and short argument for pdf file
    parser.add_argument("--gsw", help="get global software dir")

    # Add long and short argument for pdf file
    parser.add_argument("--tsw", help="type software dir")

    # Read arguments from the command line
    args = parser.parse_args()

    print(Validate(args.inst_dir, args.inst_type, args.pdf, args.gsw, args.tsw).validate())
