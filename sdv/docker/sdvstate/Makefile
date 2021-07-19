# Set the shell to bash always
SHELL := /bin/bash


#############
# Options
############

IMG_TAG="latest"
WORKDIR="workdir"

###################

# helper for printing yellow-bold formatted messages in makefile.
# Usage: $S some text message $E
S=printf "\n\e[1;33m[makefile]:
E=\e[0m\n"


define HELP_MSG

Usage: make [target] arguments=value
_________________________________________________________________
Targets:

make sandbox
	creates new sandbox container.

make sandbox-clean
	deletes sandbox container.

make build
	builds container image for sdv.

make bash
	opens a bash to sandbox contianer

make run
	runs sdvstate checks inside sandbox container.

make lint
	lints sdvstate code and generates report.

make setup-dev
	creates workdir for local developement files.

_________________________________________________________________
Optional arguments:

IMG_TAG
	Currently set to '$(IMG_TAG)'

endef
export HELP_MSG
help:
	@echo "$$HELP_MSG"


# The following target enables all commands to run in same shell. This enables
# exit to kill the program
.ONESHELL:


define CONF
## Path to PDF file
PDF_FILE: github.com/nfvid/sites/blob/master/intel-pod10.json

#############
# Airship arguments
#############

# Path to kube-config file
KUBE_CONFIG : /sdv/workdir/example/config

MASTER_ROLE_NAME : masters
WORKER_ROLE_NAME : workers
endef
export CONF
setup-dev:
	@if [ ! -d "$(WORKDIR)" ]; then \
		mkdir $(WORKDIR); \
		mkdir "$(WORKDIR)/example"; \
		echo "$$CONF" >> "$(WORKDIR)/example/conf.yaml"; \
		$S: Created local workdir. $E; \
	fi


build:
	$S: building sdv image... $E
	@docker build . -t sdv:$(IMG_TAG) -f Dockerfile


sandbox-clean:
	@if [[ "$(shell docker container ls --format "{{.Names}}" | grep sdvsandbox)" == "sdvsandbox" ]]; then \
	  docker container stop sdvsandbox; \
	fi

sandbox: build sandbox-clean
	docker container run --rm -d --name sdvsandbox \
	-v $(PWD):/sdv/ \
	-v $(PWD)/workdir/result:/tmp/state \
	sdv:latest /bin/bash -c "while true; do sleep 10; done;";


bash:
	docker container exec -it sdvsandbox /bin/bash

define sandbox_bash
	if [[ "$(shell docker container ls --format "{{.Names}}" | grep sdvsandbox)" == "" ]]; then \
		echo "Sandbox container does not exists. Creating Sandbox..."; \
		make sandbox; \
	fi
	docker container exec -it sdvsandbox bash -c $(1);
endef

run:
	@$(call sandbox_bash, "/sdv/state --conf-file /sdv/workdir/example/conf.yaml")

lint:
	@cp ../../../pylintrc $(WORKDIR)/pylintrc
	@$(call sandbox_bash, \
	"pylint --rcfile=/sdv/workdir/pylintrc /sdv/state /sdv/server /sdv/internal /sdv/tools")


test:
	@echo "Todo"

all: help


.PHONY: help setup-dev build sandbox-clean sandbox bash lint test run all 


