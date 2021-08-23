# Copyright 2020 University Of Delhi.
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
Package for Airship
"""


### Pod Health Checks
from .pod_health_check import pod_health_check

### Ceph Health Checks
from .ceph_check import ceph_health_check

### Monitoring & Logging Agents Checks
from .monitoring_logging_agent_check import prometheus_check
from .monitoring_logging_agent_check import grafana_check
# from .monitoring_logging_agent_check import prometheus_alert_manager_check
from .monitoring_logging_agent_check import elasticsearch_check
from .monitoring_logging_agent_check import kibana_check
from .monitoring_logging_agent_check import nagios_check
from .monitoring_logging_agent_check import elasticsearch_exporter_check
from .monitoring_logging_agent_check import fluentd_exporter_check

### Network Checks
from .network_check import physical_network_check

### Compute Related Checks
from .compute_check import reserved_vnf_cores_check
from .compute_check import isolated_cores_check
from .compute_check import vswitch_pmd_cores_check
from .compute_check import vswitch_dpdk_lcores_check
from .compute_check import os_reserved_cores_check
from .compute_check import nova_scheduler_filters_check
from .compute_check import cpu_allocation_ratio_check
