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

""" program which validates software profile """

import os


class SoftwareValidation():
    """ perform hardware validation """

    def __init__(self, role, json, value, manifest, global_dir, type_dir, man_dir, logger):
        # store external values
        self.role = role
        self.json = json
        self.logger = logger
        self.manifest = manifest
        # initialize internal values
        self.right = 0
        self.wrong = 0
        self.total = 0
        self.result = ""
        self.software_list = []
        # intialization functions
        self.get_software_list(global_dir, type_dir, man_dir)
        self.validate(value)

    def get_software_list(self, global_dir, type_dir, man_dir):
        """ get a list of all softwares by checking the global softwares,
            type and site specific softwares used """
        dirs = [global_dir, type_dir, man_dir]

        try:
            for direc in dirs:
                for dirpath, dirnames, filenames in os.walk(direc):
                    for filename in [f for f in filenames if f.endswith(".yaml")]:
                        temp = filename.split('.')[0]
                        temp = temp.split('-')[0]
                        self.software_list.append(temp)
        except FileNotFoundError:
            self.logger.exception(" error in accessing dirs ")
            raise

    def get_values(self):
        """ return set of right wrong and total """
        return self.right, self.wrong, self.total, self.result

    def comparison(self, key, profile, pdf_val, man_val):
        """ do comparison and print results"""
        self.total += 1
        self.logger.debug("key:%s, profile:%s, pdf_val:%s, man_val:%s, role:%s",
                          key, profile, pdf_val, man_val, self.role)

        if pdf_val == "":
            self.result += ("No value exists for pdf-key:{} of profile:{} and role:{}\n".
                            format(key, profile, self.role))
        elif man_val == []:
            self.result += ("No value exists for manifest-key:{} of profile:{} and role:{}\n".
                            format(key, profile, self.role))
        elif str(pdf_val) not in man_val:
            self.result += (
                "The pdf and manifest values do not match for key:{} profile:{} role:{}\n".format(
                    key, profile, self.role))
            self.result += ("the pdf val:{} and manifest val:{}\n".format(pdf_val, man_val))
            self.wrong += 1
        else:
            self.result += (
                "The pdf and manifest values do match for key:{} profile:{} role:{}\n".format(
                    key, profile, self.role))
            self.right += 1

    def validate(self, value):
        """ validate software profile """
        self.logger.info("started with the validation of software set:%s", value)
        val = ""
        profile = 'software_set'
        # keys = ["none"]

        for key in self.json[profile]:
            if key["set_name"] == value:
                val = key
                break
        self.logger.info("completed with the validation of software set:%s", value)

        self.validate_undercloud(val["undercloud_profile"])
        self.validate_infrastructure(val["infrasw_profile"])
        self.validate_openstack(val["openstack_profile"])

    def validate_undercloud(self, value):
        """ validate undercloud sw """
        self.logger.info("started with the validation of undercloud:%s", value)
        val = ""
        profile = 'undercloud_sw_profiles'
        keys = ["name", "version"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key
                break

        for val in val["sw_list"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = self.software_list
                self.comparison(key, profile, temp1, temp2)
        self.logger.info("completed with the validation of undercloud:%s", value)

    def validate_infrastructure(self, value):
        """ validate infra sw """
        self.logger.info("started with the validation of infra_sw:%s", value)
        val = ""
        profile = 'infra_sw_profiles'
        keys = ["name", "version"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key
                break

        for val in val["sw_list"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = self.software_list
                self.comparison(key, profile, temp1, temp2)
        self.logger.info("completed with the validation of infra_sw:%s", value)

    def validate_openstack(self, value):
        """ validate openstack sw """
        self.logger.info("started with the validation of opensatck_sw:%s", value)
        val = ""
        profile = 'openstack_sw_profiles'
        keys = ["name", "version"]

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key
                break

        for val in val["sw_list"]:
            for _, key in enumerate(keys):
                temp1 = val[key]
                temp2 = self.software_list
                self.comparison(key, profile, temp1, temp2)
        self.logger.info("completed with the validation of openstack_sw:%s", value)
