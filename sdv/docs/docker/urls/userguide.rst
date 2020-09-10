********************************************************
CIRV-SDV: Validating the URLs in the Installer Manifests
********************************************************

Supported Installer Manifest: Airship.

Building and starting the container:
* Go to folder sdv/docker/sdvurls
* Build the container with 'docker build' command. Consider naming/tagging the container properly.
* Run the container using docker run. The container creates a report under /tmp folder. Hence, consider mapping a volume to '/tmp' folder to get the report.


Interacting with the container
##############################
Inputs:

* Installer Used. Keyword: "installer". Example Value: "airship". This is mandatory
* Link to the installer manifests. Keyword: "link". Example Value: "https://gerrit.opnfv.org/gerrit/airship". This is mandatory
* Version (For Airship, this refers to Treasuremap Version). Keyword: "version". Example Value: "v1.7". This is mandatory only for Airship.
* Name of the site. Keyword: "name". Example Value: "intel-pod10". This is mandatory only for Airship

Assuming the container is running locally, the example command would be::

    curl --header "Content-Type: application/json" --redata '{"installer":"airship", "link":"https://gerrit.opnfv.org/gerrit/airship", "version":"v1.7", "name":"intel-pod10"}' http://localhost:8989/airship
