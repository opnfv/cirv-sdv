*****************************
CIRV-SDV: Security Validation
*****************************

Kali Release:
Openstack security checking, as described here: https://docs.openstack.org/security-guide/checklist.html is implemented.

This version supports following deployments:

1. Triple-O (RHOSP - openstack services run as containers)
2. Openstack on Kubernetes (Ex: Airship)
3. Legacy - Devstack (openstack sevices baremetal applications)

Running the container
#####################

run command docker build -t sdv-security .
Things to note before building

1. Correct deployment type
2. Corresponding access information.
3. Comment out the last line if the container is run interactively.

First first two can be done by adding it in security.conf, or passing them as environment variables.

Running the container
#####################

It is recommended to run interactively, using the following steps

1. docker run -it sdv-security /bin/bash
2. ./os-checklist
