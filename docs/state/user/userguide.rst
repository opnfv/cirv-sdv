====================
SDVState User Guide
====================

Currently, SDVState supports validation of Airship 1.7 and Kuberef, Kuberef, a reference implementation according to the CNTT RA-2. Before running checks you need two files:
 - kubeconfig file which gives access to clusterAPI of the cluster.
 - PDF(Pod Descriptor File) of the current the deployment.

To choose between Airship and Kuberef, you need to specify the installer using "installer_used" field in the PDF of your deployment, it can either "airship" or "kuberef".
You also need to create a config file of SDVState using the above files as values. Look at example conf-file at sdv/docker/sdvstate/settings/state.yml

To run checks use command:

 ``./state --conf-file state.yml``

The checks should complete in 11-14~ seconds.

After running checks, you can find all results at ``/tmp`` directory by default.

SDVState uses default settings stored at sdv/docker/sdvstate/settings. We can override default settings by adding those in our conf-file.

To view help and all available options with the SDVState tool check help command:
 ``./state --help``

 For properly running validation on kuberef, we need some additions to the PDF file. Take a look at the PDF file at sdv/docker/sdvstate/settings/PDF.json

 We need to add following entries in the "vim_functional" field of PDF to make the validation work properly. 

    - cpu_manager_policy: It includes the details about the cpu manager policy and it is important for the policy_checks
    - topo_manager_policy: It includes the details about the topology manager policy and it is important for the policy_checks
    - cnis_supported:  It includes list of cnis supported by the cluster and it is important for the cni_plugin_check.

