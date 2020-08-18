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

""" program to perform extrapolation """

import os
import json
import logging
import argparse
import requests
from netaddr import IPNetwork

class Extrapolate():
    """Perform extrapolation"""
    def __init__(self, pdf_fn, store_at):
        # store external values
        self.store_at = store_at
        # initialzie internal values
        self.pdf = None
        self.ip_list = []
        # initialization fucntions
        self.start_logger()
        self.download_pdf(pdf_fn)
        if self.pdf is None:
            self.read_pdf(pdf_fn)

        self.get_ip(self.get_ipmi())
        self.extrapolate()

    def download_pdf(self, pdf_fn):
        """ download pdf """
        # check pdf_fn
        if pdf_fn[:4] == "http":
            # do a requests call and get value
            try:
                req = requests.get(pdf_fn)
                self.pdf = json.loads(req.text)
            except ConnectionError:
                self.logger.exception("error downloading pdf")
                raise

    def start_logger(self):
        """ starting logging process """
        logging.basicConfig(filename='extrapolation.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

        self.logger = logging.getLogger('extrapolation')
        self.logger.info("Starting extrapolation program")

    def read_pdf(self, json_fn):
        """ read platform descritpion file """
        try:
            with open(os.path.join(json_fn)) as json_file:
                self.logger.debug("Reading the pdf file:%s", json_fn)
                self.pdf = json.loads(json_file.read())
        except IOError:
            self.logger.exception("Error while reading the pdf file")
            raise

    def save_pdf(self):
        """ save the pdf file """
        try:
            with open(os.path.join(self.store_at, 'pdf_new.json'), 'w', encoding='utf-8')\
                as json_file:
                self.logger.debug("Saving the extrapolated pdf file named: pd_new.json at:%s",\
                    self.store_at)
                json.dump(self.pdf, json_file, indent=2)
        except IOError:
            self.logger.exception("Could not save the logger file")

    def get_ipmi(self):
        """ get ipmi cidr ip """
        for val in self.pdf["networks"]:
            if val["name"] == "ipmi" or val["name"] == "ilo":
                return val["cidr"]
        return "192.168.10.0/24"

    def get_ip(self, value):
        """ get list of valid ip's"""
        self.logger.debug("getting list of ip's from %s", value)

        try:
            for _ip in IPNetwork(value):
                if str(_ip).split('.')[-1] != '0' and str(_ip).split('.')[-1] != '255':
                    self.ip_list.append(str(_ip))
        except Exception:
            self.logger.exception("error with the ip module")
            raise

    def get_ilo_info(self, count):
        """get ipmi info """
        temp = dict()
        if count > len(self.ip_list):
            self.logger.error("No ip's avaialble!")
        elif not self.pdf["extrapolation_info"]["ip_increment"].isdigit():
            self.logger.error("ip increment value is not an integer")
        else:
            temp["ip"] = self.ip_list[count * int(self.pdf["extrapolation_info"]["ip_increment"])]
            temp["user"] = self.pdf["extrapolation_info"]["ilo_user"]
            temp["password"] = self.pdf["management_info"]["city"]\
                + self.pdf["management_info"]["area_name"]\
                    + self.pdf["management_info"]["room_id"]+str(count + 1)
            self.logger.debug("ipmi info:%s", temp)
        return temp

    def extrapolate(self):
        """ Perform Extrapolation """
        self.logger.info("starting extrapolation")

        list_servers = []

        # get ipmi info
        count = 0

        for val in self.pdf["roles"]:
            num_servers = int(val["count"]) # Number of servers in the particular role.
            role = val["name"]

            for idx in range(num_servers):
                temp = dict()
                temp["role_name"] = role
                temp["device_name"] = str(role) + str(idx + 1)
                temp["az_name"] = "default"
                temp["ha_name"] = "default"

                temp["ilo_info"] = self.get_ilo_info(count)
                count += 1

                list_servers.append(temp)

        # save the pdf file
        self.pdf["servers"] = list_servers
        self.save_pdf()

        self.logger.info("Extrapolation completed!")

if __name__ == "__main__":
    # main class is for testing purposes
    # Initiate the parser
    PARSER = argparse.ArgumentParser(description="Extrapolation program")

    # Add long argument for pdf file
    PARSER.add_argument("--file", help="get pdf file name")

    # Add long argument for store_at
    PARSER.add_argument("--store_at", help="store the file at")

    # Read arguments from the command line
    ARGS = PARSER.parse_args()

    # run the code
    Extrapolate(ARGS.file, ARGS.store_at)
