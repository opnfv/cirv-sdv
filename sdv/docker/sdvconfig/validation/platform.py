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

""" program which validates platform profile """


class PlatformValidation():
    """ perform hardware validation """

    def __init__(self, role, json, value, manifest, logger):
        # store external values
        self.role = role
        self.json = json
        self.value = value
        self.logger = logger
        self.manifest = manifest
        # intialize internal values
        self.right = 0
        self.wrong = 0
        self.total = 0
        self.result = ""
        # initialization functions
        self.validate()

    def get_values(self):
        """ return set of right wrong and total """
        return self.right, self.wrong, self.total, self.result

    def comparison(self, key, profile, pdf_val, man_val):
        """ do comparison and print results"""
        self.total += 1
        self.logger.debug("key:%s, profile:%s, pdf_val:%s, man_val:%s, role:%s",
                          key, profile, pdf_val, man_val, self.role)

        if pdf_val == "":
            self.result += ("No value exists for pdf-key:{} of profile:{} and role:{}\n"\
                .format(key, profile, self.role))
        elif man_val == []:
            self.result += ("No value exists for manifest-key:{} of profile:{} and role:{}\n"\
                .format(key, profile, self.role))
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

    def validate(self):
        """ validate platform profile """
        val = ""
        profile = 'platform_profiles'
        keys = ['os', 'rt_kvm', 'kernel_version', 'kernel_parameters', 'isolated_cpus',
                'vnf_cores',
                'iommu', 'vswitch_daemon_cores', 'vswitch_type', 'vswitch_uio_driver',
                'vswitch_mem_channels', 'vswitch_socket_memory', 'vswitch_pmd_cores',
                'vswitch_dpdk_lcores', 'vswitch_dpdk_rxqs', 'vswitch_options']

        for key in self.json[profile]:
            if key["profile_name"] == self.value:
                val = key
                break

        if val == "":
            self.logger.error("Not able to find platform profile name: %s", self.value)
        else:
            for key in keys:
                try:
                    temp1 = val[key]
                    temp2 = self.manifest.find_val(self.role, profile, key)
                    self.comparison(key, profile, temp1, temp2)
                except KeyError:
                    self.logger.error(
                        "Not able to find key: %s in platform profile: %s", key, self.value)
