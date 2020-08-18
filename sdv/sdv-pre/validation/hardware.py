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

""" program which validates hardware profile """

class HardwareValidation():
    """ perform hardware validation """
    def __init__(self, role, json, value, manifest, logger):
        # store external values
        self.role = "global"
        self.json = json
        self.value = value
        self.logger = logger
        # initialize internal values
        self.right = 0
        self.wrong = 0
        self.total = 0
        self.result = ""
        # initialization functions
        self.manifest = manifest
        self.validate_hardware()

    def get_values(self):
        """ return set of right wrong and total """
        return self.right, self.wrong, self.total, self.result

    def comparison(self, key, profile, pdf_val, man_val):
        """ do comparison and print results"""
        self.total += 1
        self.logger.debug("key:%s, profile:%s, pdf_val:%s, man_val:%s, role:%s", key, profile, pdf_val, man_val, self.role)

        if pdf_val == "":
            self.result += ("No value exists for pdf-key:{} of profile:{} and role:{}\n".format(key, profile, self.role))
        elif man_val == []:
            self.result += ("No value exists for manifest-key:{} of profile:{} and role:{}\n".format(key, profile, self.role))
        elif str(pdf_val) not in man_val:
            self.result += ("The pdf and manifest values do not match for key:{} profile:{} role:{}\n".format(key, profile, self.role))
            self.result += ("the pdf val:{} and manifest val:{}\n".format(pdf_val, man_val))
            self.wrong += 1
        else:
            self.result += ("The pdf and manifest values do match for key:{} profile:{} role:{}\n".format(key, profile, self.role))
            self.right += 1

    def validate_bios_profile(self, value):
        """ validate bios profile """
        val = ""
        profile = 'bios_profile'
        keys = ['bios_version', 'bios_mode', 'bootstrap_proto', 'hyperthreading_enabled', 'bios_setting']

        self.logger.info("Starting with the validation of bios profile name:%s", value)

        for key in self.json[profile]:
            if key["profile_name"] == value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find bios profile name: %s", value)
        else:
            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(self.role, profile, key)
                    self.comparison(key, profile, temp1, temp2)
                except Exception:
                    self.logger.error("Not able to find key: %s in bios profile: %s", key, value)

            self.logger.info("Completed with the validation of bios profile name:%s", value)

    def validate_processor_profile(self, value):
        """ validate processor profile """
        val = ""
        profile = 'processor_profiles'
        keys = ['speed', 'model', 'architecture']

        self.logger.info("Starting with the validation of processor profile:%s", value)

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find processor profile name: %s", value)
        else:
            val = val["profile_info"]
            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(self.role, profile, key)
                    self.comparison(key, profile, temp1, temp2)
                except Exception:
                    self.logger.error("Not able to find key: %s in processor profile: %s", key, value)
            self.logger.info("Completed with the validation of processor profile:%s", value)

    def validate_disks_profile(self, value):
        """ validate disks profile """
        val = ""
        profile = 'disks_profiles'
        keys = ['address', 'dev_type', 'rotation', 'bus']

        self.logger.info("Starting with the validation of disks profile:%s", value)

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find disk profile name: %s", value)
        else:
            val = val["profile_info"]
            for vals in val:
                for key in keys:
                    try:
                        temp1 = vals[key]
                        temp2 = self.manifest.find_val(self.role, profile, key)
                        self.comparison(key, profile, temp1, temp2)
                    except Exception:
                        self.logger.error("Not able to find key: %s in disk profile: %s", key, value)
            self.logger.info("Completed with the validation of disks profile:%s", value)

    def validate_nic_profile(self, value):
        """ validate nic profile """
        val = ""
        profile = 'nic_profiles'
        keys = ['address', 'dev_type', 'bus', 'sriov_capable', 'numa_id']

        self.logger.info("Starting with the validation of nic profile:%s", value)

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find nic profile name: %s", value)
        else:
            val = val["profile_info"]

            for vals in val:
                for key in keys:
                    try:
                        temp1 = vals[key]
                        temp2 = self.manifest.find_val(self.role, profile, key)
                        self.comparison(key, profile, temp1, temp2)
                    except Exception:
                        self.logger.error("Not able to find key: %s in nic profile: %s", key, value)
            self.logger.info("Completed with the validation of nic profile:%s", value)

    def validate_hardware(self):
        """ validate hardware """
        # find hardware profile with given key
        val = ""
        profile = 'hardware_profiles'
        keys = ['manufacturer', 'model', 'generation', 'memory']

        self.logger.info("Starting with the validation of hardware profile:%s", self.value)

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find hardware profile name: %s", self.value)
        else:
            val = val["profile_info"]

            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(self.role, profile, key)
                    self.comparison(key, profile, temp1, temp2)
                except Exception:
                    self.logger.error("Not able to find key: %s in hardware profile: %s", key, self.value)
            self.logger.info("Completed with the validation of hardware profile:%s", self.value)

        self.validate_bios_profile(val["bios_profile"])
        self.validate_processor_profile(val["processor_profile"])
        self.validate_disks_profile(val["disks_profile"])
        self.validate_nic_profile(val["nics_profile"])
