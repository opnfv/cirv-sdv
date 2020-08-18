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

# pylint: disable=line-too-long, invalid-name, missing-module-docstring, broad-except

""" manifest code """

import os
import json
import yaml
import sys

CWD = os.getcwd()

class Manifest():
    """ All about manifest """
    def __init__(self, inst_dir, mapping_file_dir, logger):
        self.yaml = dict()
        self.mapping = dict()
        self.vals = []
        self.saver = dict()
        self.logger = logger

        self.auto_generate_mapping(mapping_file_dir, inst_dir)

    def read_yaml(self, yaml_dir):
        """ read yaml file """
        yaml_files = [pos_json for pos_json in os.listdir(yaml_dir) if pos_json.endswith('.yaml')]
        temp = []

        for yaml_fn in yaml_files:
            try:
                self.logger.debug("the yaml fn:%s", yaml_fn)
                with open(os.path.join(yaml_dir, yaml_fn)) as yaml_file:
                    temp_yaml = list(yaml.load_all(yaml_file, Loader=yaml.FullLoader))
                    temp.append(temp_yaml)
            except Exception as e:
                self.logger.critical("could not read the manifest files:%s", e, exc_info=True)
                raise

        self.logger.debug("temp variable size in read_yaml:%s",len(temp))
        if len(temp) == 0:
            self.logger.critical("could not read the manifest files:%s", e, exc_info=True)
            sys.exit()

        return temp

    def get_host_profile_mapping(self, inst_dir):
        """ get host profile mapping """
        # first read the nodes.yaml file from baremetal directory
        temp_yaml = self.read_yaml(os.path.join(inst_dir, "baremetal"))
        host_profile_mapping = dict()
        
        for vals in temp_yaml:
            for val in vals:
                self.logger.info("val:%s", val)
                val = val["data"]
                host_profile_mapping[val["host_profile"]] = []

                for role in val["metadata"]["tags"]:
                    if role not in host_profile_mapping[val["host_profile"]]:
                        host_profile_mapping[val["host_profile"]].append(role)
            self.logger.info("host profile mapping values:%s", host_profile_mapping)

        return host_profile_mapping

    def read_mapping(self, mapping_file):
        """ read corresponding mapping file """
        try:
            with open(mapping_file) as mapping_file:
                temp = json.load(mapping_file)
                return temp
        except Exception as e:
            self.logger.critical("could not read the mapping file:%s", e, exc_info=True)
            raise

    def auto_generate_mapping(self, mapping_file_dir, inst_dir):
        """ generate mapping """
        # first check if the required files exist in the site
        if not os.path.exists(os.path.join(inst_dir, "baremetal")):
            self.logger.crititcal("baremetal file does not exist")
            raise FileNotFoundError("baremetal file does not exist")
        if not os.path.exists(os.path.join(inst_dir, "profiles")):
            self.logger.crititcal("profiles file does not exist")
            raise FileNotFoundError("profiles file does not exist")

        # get host profile mapping
        host_profile_mapping = self.get_host_profile_mapping(inst_dir)
        
        # first check for hardware profile
        # read the hardware mapping file, set the manifest context as hardware-intel-pod10
        
        temp = self.read_yaml(os.path.join(inst_dir, "profiles", "hardware"))
        for val in temp:
            self.yaml[val[0]["metadata"]["name"]] = val
            context = "global"
            manifest_context = val[0]["metadata"]["name"]

            temp_mapping = self.read_mapping(os.path.join(mapping_file_dir, "hardware-mapping.json"))

            for key in temp_mapping.keys():
                new_key = context + "-" + key
                self.mapping[new_key] = dict()
                self.mapping[new_key]["manifest_key"] = temp_mapping[key]["manifest_key"]
                self.mapping[new_key]["manifest_context"] = manifest_context
        
        # platform profile
        temp = self.read_yaml(os.path.join(inst_dir, "profiles", "host"))
        # self.logger.info("host manifest file output(platform):%s", temp)
        for val in temp:
            try:
                self.yaml[val[0]["metadata"]["name"]]
            except:
                self.yaml[val[0]["metadata"]["name"]] = val

            for key in host_profile_mapping:
                if key == val[0]["metadata"]["name"]:
                    for role in host_profile_mapping[key]:
                        context = role
                        manifest_context = val[0]["metadata"]["name"]

                        temp_mapping = self.read_mapping(os.path.join(mapping_file_dir, "platform-mapping.json"))

                        for key in temp_mapping.keys():
                            new_key = context + "-" + key
                            self.mapping[new_key] = dict()
                            self.mapping[new_key]["manifest_key"] = temp_mapping[key]["manifest_key"]
                            self.mapping[new_key]["manifest_context"] = manifest_context
        
        # storage profile
        temp = self.read_yaml(os.path.join(inst_dir, "profiles", "host"))
        for val in temp:
            try:
                self.yaml[val[0]["metadata"]["name"]]
            except:
                self.yaml[val[0]["metadata"]["name"]] = val

            for key in host_profile_mapping:
                if key == val[0]["metadata"]["name"]:
                    for role in host_profile_mapping[key]:
                        context = role
                        manifest_context = val[0]["metadata"]["name"]

                        temp_mapping = self.read_mapping(os.path.join(mapping_file_dir, "storage-mapping.json"))

                        for key in temp_mapping.keys():
                            new_key = context + "-" + key
                            self.mapping[new_key] = dict()
                            self.mapping[new_key]["manifest_key"] = temp_mapping[key]["manifest_key"]
                            self.mapping[new_key]["manifest_context"] = manifest_context
        
        # network profile
        temp = self.read_yaml(os.path.join(inst_dir, "networks", "physical"))
        for vals in temp:
            for val in vals:

                if val["metadata"]["name"] not in self.yaml.keys():
                    self.yaml[val["metadata"]["name"]] = []
                    self.yaml[val["metadata"]["name"]].append(val)
                else:
                    self.yaml[val["metadata"]["name"]].append(val)


                context = val["metadata"]["name"]
                manifest_context = val["metadata"]["name"]

                temp_mapping = self.read_mapping(os.path.join(mapping_file_dir, "network-mapping.json"))

                for key in temp_mapping.keys():
                    new_key = context + "-" + key
                    self.mapping[new_key] = dict()
                    self.mapping[new_key]["manifest_key"] = temp_mapping[key]["manifest_key"]
                    self.mapping[new_key]["manifest_context"] = manifest_context
            
        # info profile
        self.logger.debug("yaml file:%s", self.yaml)
        temp = self.read_yaml(os.path.join(inst_dir, "profiles", "host"))
        for val in temp:
            try:
                self.yaml[val[0]["metadata"]["name"]]
            except:
                self.yaml[val[0]["metadata"]["name"]] = val

            for key in host_profile_mapping:
                if key == val[0]["metadata"]["name"]:
                    for role in host_profile_mapping[key]:
                        context = role
                        manifest_context = val[0]["metadata"]["name"]

                        temp_mapping = self.read_mapping(os.path.join(mapping_file_dir, "info-mapping.json"))

                        for key in temp_mapping.keys():
                            new_key = context + "-" + key
                            self.mapping[new_key] = dict()
                            self.mapping[new_key]["manifest_key"] = temp_mapping[key]["manifest_key"]
                            self.mapping[new_key]["manifest_context"] = manifest_context
        
        self.logger.debug("the autogenrated mapping:%s", self.mapping)
        self.logger.info("Completed autogenration of mapping")

    def find_vals(self, key, temp_json):
        """ insert all matching json key-vals in array """
        # self.logger.info("temp_json value:%s", temp_json)
        for k, v in temp_json.items():
            if k == key:
                if isinstance(v, list):
                    for val in v:
                        self.vals.append(str(val))
                else:
                    self.vals.append(str(v))

            if isinstance(v, dict):
                found = self.find_vals(key, v)
                if found:
                    return True

            if isinstance(v, list):
                for _, val in enumerate(v):
                    if isinstance(val, str):
                        continue
                    found = self.find_vals(key, val)
                    if found:
                        return True
        return False

    def find_val(self, role, context, skey):
        """ find val in manifest """

        # 1. find corresponding manifest context & key
        # code here
        key = role + "-" + context + "-" + skey
        man_con = dict()
        man_key = dict()
        self.vals = []

        try:
            return self.saver[key]
        except Exception:
            # log that the key does not exist in the saver dict.
            self.logger.info("key: %s doesnt exist in the saved keys, searching manifest")

        try:
            man_con = self.mapping[key]["manifest_context"]
            man_key = self.mapping[key]["manifest_key"]
        except:
            self.logger.error("could not find corresponding mapping for key:%s", key)
            return self.vals

        if man_con == '':
            self.saver[key] = []
            return []

        # 2. find values corresponding to the key( by recursing through shortened dict )
        # code here
        temp = self.yaml[man_con]
        # print(man_key,temp)
        if isinstance(temp, list):
            temp_json = dict()
            temp_json[man_con] = temp
            self.find_vals(man_key, temp_json)
        else:
            self.find_vals(man_key, json)
        
        if self.vals == []:
            self.logger.debug("found nothing for man_con:%s and man_key:%s and key:%s", man_con, man_key, key)

        # 3. return the value
        self.saver[key] = self.vals
        return self.vals
