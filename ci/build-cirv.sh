#!/bin/bash
#
# Copyright 2020-2018 Spirent Communications, Intel Corporation., Tieto
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

# CIRV build execution script

# Usage:
#       build-cirv.sh job_type
#   where job_type is one of "verify", "merge", "daily"
# Version-1: 'verify'

#
# exit codes
#

EXIT=0
EXIT_SANITY_FAILED=1
EXIT_PYLINT_FAILED=2

#
# configuration
#

SWV_BIN="./sdv/valid"
LOG_FILE_PREFIX="/tmp/cirv_build"
DATE=$(date -u +"%Y-%m-%d_%H-%M-%S")
BRANCH=${GIT_BRANCH##*/}
CIRVENV_DIR="$HOME/cirvenv"
# WORKSPACE="./"

#
# main
#

echo

# enter workspace dir
cd $WORKSPACE


# create virtualenv if needed
if [ ! -e $CIRVENV_DIR ] ; then
    echo "Create CIRV environment"
    echo "========================="
    virtualenv --python=python3 "$CIRVENV_DIR"
    echo
fi

# acivate and update virtualenv
echo "Update CIRV environment"
echo "========================="
source "$CIRVENV_DIR"/bin/activate
pip install -r ./requirements.txt
echo


# execute pylint to check code quality
function execute_cirv_pylint_check {
    if ! ./check -b ; then
        EXIT=$EXIT_PYLINT_FAILED
    fi
}

# verify basic cirv functionality
function execute_cirv_sanity {
    DATE_SUFFIX=$(date -u +"%Y-%m-%d_%H-%M-%S")
    LOG_FILE="${LOG_FILE_PREFIX}_sanity_${DATE_SUFFIX}.log"
    echo "Execution of CIRV sanity checks:"
    for PARAM in '--version' '--help'; do
        echo -e "------------------------------------------------" >> $LOG_FILE
        echo "$SWV_BIN $PARAM " >> $LOG_FILE
        echo -e "------------------------------------------------" >> $LOG_FILE
        $SWV_BIN $PARAM &>> $LOG_FILE
        if $SWV_BIN $PARAM &>> $LOG_FILE ; then
            printf "    %-70s %-6s\n" "$SWV_BIN $PARAM" "OK"
        else
            printf "    %-70s %-6s\n" "$SWV_BIN $PARAM" "FAILED"
            EXIT=$EXIT_SANITY_TC_FAILED
        fi
        echo >> $LOG_FILE
    done
}

# execute job based on passed parameter
case $1 in
    "verify")
        echo "================="
        echo "CIRV verify job"
        echo "================="

        execute_cirv_pylint_check
        execute_cirv_sanity

        exit $EXIT
        ;;
    "merge")
        echo "================"
        echo "CIRV merge job"
        echo "================"

        exit $EXIT
        ;;
    *)
        echo "================"
        echo "CIRV daily job"
        echo "================"

        exit $EXIT
        ;;
esac

exit $EXIT
