====================
SDVState User Guide
====================

Currently, SDVState supports validation of Airship 1.7. Before running checks you need two files:
 - kubeconfig file which gives access to clusterAPI of Airship cluster.
 - PDF(Pod Descriptor File) of the current Airship deployment.

Create a config file of SDVState using the above files as values. Look at example conf-file at sdv/docker/sdvstate/example/state.yml

To run checks use command:

 ``./state --conf-file state.yml``

The checks should complete in 11-14~ seconds.

After running checks, you can find all results at ``/tmp`` directory by default.

SDVState uses default settings stored at sdv/docker/sdvstate/settings. We can override default settings by adding those in our conf-file.

To view help and all available options with the SDVState tool check help command:
 ``./state --help``