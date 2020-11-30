=========================
SDVState Developer Guide
=========================

The Top-level directory of consists following flies:

.. code-block:: bash

    sdvstate
    ├── core
    ├── settings
    ├── tools
    ├── validator
    ├── state
    ├── server
    └── dockerfile

``state`` is the entry point of the SDVState testing tool.

``validator`` consists of different implementations of sdvstate tool. For example, one implementation can be for validation of Airship while others can validate TripleO, Kuberef and so on.

``tools`` consists of any third party utilities code or other tools utilites maintained by the project.

``settings`` consists of a bunch of yaml files with default configuration parameters used by SDVState tool. These settings can be overridden by the user in their conf-file. Precedence of settings loaded by SDVState tool: ``cli > env > conf-file > settings-dir``. Have a look at :doc:`settings tool <settings>` to see how settings are managed across SDVState tool.

``core`` consists of all other code used to build the SDVState tool itself like displaying Reports, loading PDFs, etc..

Managing Results
^^^^^^^^^^^^^^^^
SDVState maintains result-api module for managing results of checks. Located at ``sdvstate/tools/result_api``. Have a look at :doc:`Result API documentation <result_api>`

Result of every check should have the format:

.. code-block:: bash

  {
        "case_name": "name_of_check",
        "category": "storage",
        "criteria": "pass",
        "details": { .. any number of values ..}
  }

Where criteria must be either ``pass`` or ``fail``. While ``details`` can have any value or values related to results. All four keys are mandatory while reporting the results of individual checks.

All results are stored in ``results.json`` file which consists an array of check results.

Note one of the result items in an array is the overall result which consists summary of all checks. It also consists of other details and matches the format of TestAPI of OPNFV. These are also the values that are exported to TestAPI by the tool.