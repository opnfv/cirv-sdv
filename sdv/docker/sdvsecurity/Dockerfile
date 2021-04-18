# Run this tool as a container.
FROM python:3.9.2-slim-buster

RUN apt-get update && apt-get -y install vim && pip install paramiko kubernetes scp
COPY nfvsec /nfvsec/
COPY k8sconfig /conf/
COPY pki /conf/pki/

WORKDIR /nfvsec
