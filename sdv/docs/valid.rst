.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Intel Corporation, AT&T and others.

CIRV Software Validation Tool
=============================
This tool is designed to perform Software Configuration Validation, which covers:

1. Pre-Deployment (of VIM or Container Management Software) Validation of Software Configuration
2. Post-Deployment (of VIM or Container Management Software) Validation of Software Configuration
3. Network-Link Checking - Validating VLAN and IP configurations


Installation
************
This tool does not have any installation. However, there are requirements in terms of Python packages, which can be installed using pip3. Refer to requirements.txt file for the package list.

Usage
*****
Example Commands:

1. To run all the validations: ./valid
2. Help: ./valid --help
3. Version Check: ./valid --version
4. List Sofware Pre-Deployment validators: ./valid --list-swpredepv
5. List Sofware Post-Deployment validators: ./valid --list-swpostdepv
6. List all validations: ./valid --list-validations
7. Run only single validation [WORK IN PROGRESS]
