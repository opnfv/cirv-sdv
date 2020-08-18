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

# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-branches

""" program which validates network profile """


class NetworkValidation():
    """ perform network validation """

    def __init__(self, role, json, value, manifest, logger):
        # store external state
        self.role = role
        self.json = json
        self.value = value
        self.logger = logger
        self.manifest = manifest
        # initialize internal state
        self.right = 0
        self.wrong = 0
        self.total = 0
        self.result = ""
        # initialization functions
        self.validate_network()

    def get_values(self):
        """ return set of right wrong and total """
        return self.right, self.wrong, self.total, self.result

    def comparison(self, key, profile, pdf_val, man_val, role):
        """ do comparison and print results"""
        self.total += 1
        self.logger.debug("key:%s, profile:%s, pdf_val:%s, man_val:%s, role:%s",
                          key, profile, pdf_val, man_val, role)

        if pdf_val == "":
            self.result += ("No value exists for pdf-key:{} of profile:{} and role:{}\n"\
                .format(key, profile, role))
        elif man_val == []:
            self.result += ("No value exists for manifest-key:{} of profile:{} and role:{}\n"\
                .format(key, profile, role))
        elif str(pdf_val) not in man_val:
            self.result += (
                "The pdf and manifest values do not match for key:{} profile:{} role:{}\n".format(
                    key, profile, role))
            self.result += ("the pdf val:{} and manifest val:{}\n".format(pdf_val, man_val))
            self.wrong += 1
        else:
            self.result += (
                "The pdf and manifest values do match for key:{} profile:{} role:{}\n".format(
                    key, profile, role))
            self.right += 1

    def validate_networks(self, value):
        """ validate network link """
        self.logger.info("Starting with the validation of networks profile:%s", value)
        val = ""
        profile = 'networks'
        keys = [
            'name',
            'tunnel_type',
            'tunnel_id',
            'tunnel_id_range',
            'mtu',
            'routedomain',
            'cidr',
            'dns',
            'v6_cidr']

        self.logger.info("Starting with the validation of network profile:%s", value)

        for key in self.json[profile]:
            if key["name"] == value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find network profile name: %s", value)
        else:
            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(value, profile, key)
                    self.comparison(key, profile, temp1, temp2, value)
                except KeyError:
                    self.logger.error("Not able to find key: %s in network profile: %s", key, value)

            keys = ["name", "ip"]

            for item in val["vips"]:
                for key in keys:
                    try:
                        temp1 = item[key]
                        temp2 = self.manifest.find_val(value, profile + '.vips', key)
                        self.comparison(key, profile, temp1, temp2, value)
                    except KeyError:
                        self.logger.error(
                            "Not able to find key: %s in network.vips profile: %s", key, value)

            keys = ["subnet", "gateway", "metric", "routedomain"]

            for item in val["routes"]:
                for key in keys:
                    try:
                        temp1 = item[key]
                        temp2 = self.manifest.find_val(value, profile + '.routes', key)
                        self.comparison(key, profile, temp1, temp2, value)
                    except KeyError:
                        self.logger.error(
                            "Not able to find key: %s in network.routes profile: %s", key, value)

            keys = ["type", "start", "end"]

            for item in val["allocation_pools"]:
                for key in keys:
                    try:
                        temp1 = item[key]
                        temp2 = self.manifest.find_val(value, profile + '.allocation_pools', key)
                        self.comparison(key, profile, temp1, temp2, value)
                    except KeyError:
                        self.logger.error(
                            "Not able to find key: %s in network.allocation_pools profile: %s"\
                                , key, value)

            keys = ["type", "start", "end"]

            for item in val["v6_allocation_pools"]:
                for key in keys:
                    try:
                        temp1 = item[key]
                        temp2 = self.manifest.find_val(value, profile + '.v6_allocation_pools', key)
                        self.comparison(key, profile, temp1, temp2, value)
                    except KeyError:
                        self.logger.error(
                            "Not able to find key: %s in network.v6_allocation_pools profile: %s"\
                                , key, value)
            self.logger.info("Completed with the validation of networks profile:%s", value)

    def validate_network_link(self, value):
        """ validate network link """
        self.logger.info("Starting with the validation of network link:%s", value)
        val = ""
        profile = 'network_link'
        keys = [
            'name',
            'type',
            'bonding_mode',
            'mtu',
            'linkspeed',
            'trunking_mode',
            'trunking_default_nw',
            'vid',
            'vf_count']

        self.logger.info("Starting with the validation of network link:%s", value)

        for key in self.json[profile]:
            if key["name"] == value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find network link name: %s", value)
        else:
            val = val["profile_info"]

            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(value, profile, key)
                    self.comparison(key, profile, temp1, temp2, value)
                except KeyError:
                    self.logger.error(
                        "Not able to find key: %s in network link profile: %s", key, value)

            keys = ["key", "value"]

            for key in keys:
                try:
                    temp1 = val["metadata"][key]
                    temp2 = self.manifest.find_val(value, profile + '.metadata', key)
                    self.comparison(key, profile, temp1, temp2, value)
                except KeyError:
                    self.logger.error(
                        "Not able to find key: %s in network link.metadata profile: %s", key, value)

            keys = ["name", "type"]

            for key in keys:
                try:
                    temp1 = val["members"][key]
                    temp2 = self.manifest.find_val(value, profile + '.members', key)
                    self.comparison(key, profile, temp1, temp2, value)
                except KeyError:
                    self.logger.error(
                        "Not able to find key: %s in network link.metadata profile: %s", key, value)
        self.logger.info("completed with the validation of network link:%s", value)

    def validate_network(self):
        """ validate network """
        # find in interface mapping profile with given key
        val = ""
        profile = 'interface_mapping_profiles'

        self.logger.info("Starting with the validation of interface mapping profile:%s", self.value)

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find interface profile name: %s", self.value)
        else:
            val = val["profile_data"]

            for item in val:
                try:
                    self.validate_network_link(item["interface_name"])
                    self.logger.info("networks:%s", item["networks"])
                    for smaller_item in item["networks"]:
                        self.validate_networks(smaller_item["name"])
                except KeyError:
                    self.logger.exception(
                        "Not able to find key in interface mapping profile profile:%s", self.value)
            self.logger.info(
                "Completed with the validation of interface mapping profile:%s",
                self.value)
