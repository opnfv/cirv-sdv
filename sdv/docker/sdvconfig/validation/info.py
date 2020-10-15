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

# pylint: disable=too-many-instance-attributes, too-many-statements

""" validate general info of pdf """


class InfoValidation():
    """ perform hardware validation """

    def __init__(self, json, manifest, logger):
        # store external state
        self.role = 'masters'
        self.json = json
        self.logger = logger
        self.manifest = manifest
        # initialize internal state
        self.right = 0
        self.wrong = 0
        self.total = 0
        self.result = ""
        # initialization function
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
        """ validate all infos """
        self.logger.info("starting info validation")
        val = ""
        profile = 'management_info'
        keys = ['owner', 'area_name', 'area_center_name', 'room_id', 'city', 'resource_pool_name']

        val = self.json[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'ntp_info'
        keys = ['primary_ip', 'primary_zone', 'secondary_ip', 'secondary_zone']

        val = self.json[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'syslog_info'
        keys = ["server_ip", "transport"]

        val = self.json[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        # val = ""
        # profile = 'ldap_info'
        # keys = ["base_url", "url", "auth_path", "common_name", "subdomain", "domain"]

        # val = self.json[profile]
        # for key in keys:
        #     temp1 = val[key]
        #     temp2 = self.manifest.find_val(self.role, profile, key)
        #     self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'proxy_info'
        keys = ["address", "port", "user", "password"]

        val = self.json[profile]
        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'vim_info'
        keys = [
            "vim_name",
            "vim_id",
            "vendor",
            "version",
            "installer",
            "deployment_style",
            "container_orchestrator",
            "storage_type"]

        val = self.json[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'deployment_info'
        keys = [
            "high_availability",
            "introspection",
            "deployment_type",
            "installer_used",
            "workload_vnf",
            "workload_cnf",
            "sdn_controller",
            "sdn_controller_version",
            "sdn_controller_nbapps",
            "vnfm",
            "vnfm_version",
            "data_plane_used",
            "ironic_deploy_interface",
            "external_storage_cluster",
            "bl_str_connect_method",
            "cpu_allocation_ratio"]

        val = self.json[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        val = ""
        profile = 'jumphost_info'
        keys = ["ip", "name"]

        val = self.json[profile]

        for key in keys:
            temp1 = val[key]
            temp2 = self.manifest.find_val(self.role, profile, key)
            self.comparison(key, profile, temp1, temp2)

        # val = ""
        # profile = 'rack_info.rack_details'
        # keys = ["rack_name","rack_description", "raack_az"]

        # val = self.json["rack_info"]["rack_split"]

        # for key in keys:
        #     temp1 = val[key]
        #     temp2 = self.manifest.find_val(self.role, profile, key)
        #     self.comparison(key, profile, temp1, temp2)

        # val = ""
        # profile = 'storage_cluster_info'
        # keys = ["name", "cluster_type", "cluster_id", "auth_type", "username", "password", \
        # "certificate_location", "client_key", "public_cidr", "cluster_cidr"]

        # val = self.json[profile]

        # for key in keys:
        #     temp1 = val[key]
        #     temp2 = self.manifest.find_val(self.role, profile, key)
        #     self.comparison(key, profile, temp1, temp2)
        self.logger.info("completing info validation")
