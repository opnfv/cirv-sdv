# Copyright 2020 Spirent Communications.
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

"""
Create Components.
"""


def create_swpreurlsvalidator(swpreurlsvalidator_class):
    """ Create Pre-Links Validators"""
    return swpreurlsvalidator_class()


def create_swpoststatevalidator(swpoststatevalidator_class):
    """ Create Post-State Validators"""
    return swpoststatevalidator_class()


def create_nwlinksvalidator(nwlinksvalidator_class):
    """ Create NW Link-Validators"""
    return nwlinksvalidator_class()


def create_swpreconfigvalidator(swpreconfigvalidator_class):
    """ Create Pre-Config Validators"""
    return swpreconfigvalidator_class()


def create_swpostsecurityvalidator(swpostsecurityvalidator_class):
    """ Create Post-Security Validators"""
    return swpostsecurityvalidator_class()


def create_resmodvalidator(resmodvalidator_class):
    """ Create Resource-Model Validators"""
    return resmodvalidator_class()
