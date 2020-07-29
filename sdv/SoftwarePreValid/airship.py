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
Airship implementation of Software Predeployment Validation
"""

import os
import shutil
from pathlib import Path
import git
import urllib3
import yaml
from conf import settings
from SoftwarePreValid import swprevalidator


def check_link(link):
    """
    Function the check the availability of Hyperlinks
    """
    timeout = urllib3.util.Timeout(connect=5.0, read=7.0)
    http = urllib3.PoolManager(timeout=timeout)
    try:
        http.request('HEAD', link)
    except urllib3.exceptions.LocationValueError as err:
        print(err.args)
        return False
    except urllib3.exceptions.MaxRetryError as err:
        print(err.args)
        return False
    except urllib3.exceptions.RequestError as err:
        print(err.args)
        return False
    except urllib3.exceptions.ConnectTimeoutError as err:
        print(err.args)
        return False
    except urllib3.exceptions.PoolError as err:
        print(err.args)
        return False
    except urllib3.exceptions.HTTPError as err:
        print(err.args)
        return False
    return True


class Airship(swprevalidator.ISwPreValidator):
    """
    Ariship Sw Validation
    """
    def __init__(self):
        """ Airship class constructor """
        super().__init__()
        self.url = settings.getValue('AIRSHIP_MANIFEST_URL')
        self.branch = settings.getValue('AIRSHIP_MANIFEST_BRANCH')
        self.dl_path = settings.getValue('AIRSHIP_MANIFEST_DOWNLOAD_PATH')
        self.site_name = settings.getValue('AIRSHIP_MANIFEST_SITE_NAME')
        self.manifest = None
        self.dirpath = Path(self.dl_path, 'airship')
        self.tmdirpath = Path(self.dl_path, 'treasuremap')
        self.locations = []

    def clone_repo(self):
        """
        Cloning the repos
        """
        git.Repo.clone_from(self.url,
                            self.dirpath,
                            branch=self.branch)
        git.Repo.clone_from('https://github.com/airshipit/treasuremap',
                            self.tmdirpath,
                            branch=settings.getValue(
                                'AIRSHIP_TREASUREMAP_VERSION'))

    def cleanup_manifest(self):
        """
        Remove existing manifests
        """
        # Next Remove any manifest files, if it exists
        if self.dirpath.exists() and self.dirpath.is_dir():
            shutil.rmtree(self.dirpath)
        if self.tmdirpath.exists() and self.tmdirpath.is_dir():
            shutil.rmtree(self.tmdirpath)

    def manifest_exists_locally(self):
        """
        Check if manifests exists locally
        """
        if self.dirpath.exists() and self.dirpath.is_dir():
            return True
        return False

    def validate_hyperlinks(self):
        """
        Hyperlink Validation
        """
        self.cleanup_manifest()
        # Next, clone the repo to the provided path.
        self.clone_repo()

        if self.dirpath.exists() and self.dirpath.is_dir():
            # Get the file(s) where links are defined.
            self.find_locations(
                os.path.join(self.dirpath, 'type',
                             'cntt', 'software',
                             'config', 'versions.yaml'))
            for location in self.locations:
                if check_link(location):
                    print("The Link: %s is VALID" % (location))
                else:
                    print("The Link: %s is INVALID" % (location))

    # pylint: disable=consider-using-enumerate
    def find_locations(self, yamlfile):
        """
        Find all the hyperlinks in the manifests
        """
        with open(yamlfile, 'r') as filep:
            lines = filep.readlines()
            for index in range(len(lines)):
                line = lines[index].strip()
                if line.startswith('location:'):
                    link = line.split(":", 1)[1]
                    if "opendev" in link:
                        if ((len(lines) > index+1) and
                                (lines[index+1].strip().startswith(
                                    'reference:'))):
                            ref = lines[index+1].split(":", 1)[1]
                            link = link + '/commit/' + ref.strip()
                    if link.strip() not in self.locations:
                        print(link)
                        self.locations.append(link.strip())
                if 'docker.' in line:
                    link = line.split(":", 1)[1]
                    link = link.replace('"', '')
                    parts = link.split('/')
                    if len(parts) == 3:
                        link = ('https://index.' +
                                parts[0].strip() +
                                '/v1/repositories/' +
                                parts[1] + '/' + parts[2].split(':')[0] +
                                '/tags/' + parts[2].split(':')[-1])
                        if link.strip() not in self.locations:
                            print(link)
                            self.locations.append(link.strip())

    # pylint: disable=too-many-nested-blocks, too-many-boolean-expressions
    def validate_configuration_mandatory(self):
        """
        Configuration checking of mandatory parameters
        """
        if not self.manifest_exists_locally():
            self.clone_repo()
        # We will perform validation one-by-one:
        # The Operating System Flavor
        os_done = False
        os_filename = os.path.join(self.tmdirpath,
                                   'global',
                                   'software',
                                   'charts',
                                   'ucp',
                                   'drydock',
                                   'maas.yaml')
        with open(os_filename, 'r') as osref:
            osfiles = yaml.load_all(osref, Loader=yaml.FullLoader)
            for osf in osfiles:
                if ('data' in osf and
                        'values' in osf['data'] and
                        'conf' in osf['data']['values'] and
                        'maas' in osf['data']['values']['conf'] and
                        'images' in osf['data']['values']['conf']['maas'] and
                        ('default_os' in
                         osf['data']['values']['conf']['maas']['images'])):
                    if (settings.getValue('OPERATING_SYSTEM') in
                            osf['data']['values']['conf']['maas']['images'][
                                'default_os']):
                        print('Operating System is VALID')
                        os_done = True
        if not os_done:
            print("Operating System is INVALID")

        filesdir = os.path.join(self.dirpath,
                                'site',
                                self.site_name,
                                'profiles',
                                'host')
        hostprofile = None
        os_ver_done = False
        if os.path.isdir(filesdir):
            for filename in os.listdir(filesdir):
                filename = os.path.join(filesdir, filename)
                with open(filename, 'r') as fileref:
                    hostprofile = yaml.load(fileref, Loader=yaml.FullLoader)
                if 'data' in hostprofile:
                    if 'platform' in hostprofile['data']:
                        if 'image' in hostprofile['data']['platform']:
                            if (hostprofile['data']['platform']['image'] in
                                    settings.getValue('OS_VERSION_NAME')):
                                print('Operating System Version is VALID')
                                os_ver_done = True
                                break
        if not os_ver_done:
            print("Operating System Version is INVALID")
        # Virtualization - Hugepages and CPU Isolation
        hugepages_size_done = False
        hugepages_count_done = False
        filesdir = os.path.join(self.dirpath,
                                'type',
                                'cntt',
                                'profiles',
                                'hardware')
        if os.path.isdir(filesdir):
            for filename in os.listdir(filesdir):
                filename = os.path.join(filesdir, filename)
                with open(filename, 'r') as fileref:
                    hwprofile = yaml.load(fileref, Loader=yaml.FullLoader)
                if ('data' in hwprofile and
                        'hugepages' in hwprofile['data'] and
                        'dpdk' in hwprofile['data']['hugepages']):
                    if ('size' in hwprofile['data']['hugepages']['dpdk'] and
                            (settings.getValue('HUGEPAGES_SIZE') in
                             hwprofile['data']['hugepages']['dpdk']['size'])):
                        print('Hugepages Size is VALID')
                    else:
                        print('Hugepages Size is INVALID')
                        hugepages_size_done = True
                    if ('count' in hwprofile['data']['hugepages']['dpdk'] and
                            (settings.getValue('HUGEPAGES_COUNT') ==
                             hwprofile['data']['hugepages']['dpdk']['count'])):
                        print('Hugepages COUNT is VALID')
                    else:
                        print('Hugepages COUNT is INVALID')
                        hugepages_count_done = True
                if hugepages_size_done and hugepages_count_done:
                    break

        # Virtual Switch - Switch and Configuration
        # Openstack-Version
        filename = os.path.join(self.tmdirpath,
                                'global',
                                'software',
                                'config',
                                'versions.yaml')
        if os.path.exists(filename):
            if settings.getValue('OPENSTACK_VERSION') in open(filename).read():
                print('Openstack Version is valid')
            else:
                print('Openstack version if INVALID')
        # Openstack Services
        # Bootstrap

    def validate_configuration_optional(self):
        """
        Validate Optional COnfigurations
        """
        return False
