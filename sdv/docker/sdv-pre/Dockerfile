FROM python:3.8-slim-buster

MAINTAINER Ashwin Nayak <ashwinnayak111@gmail.com>

RUN mkdir sdv-pre
WORKDIR /sdv-pre/

COPY requirements.txt /sdv-pre/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY extrapolation/ /sdv-pre/extrapolation/
COPY mapping/ /sdv-pre/mapping/
COPY validation/ /sdv-pre/validation/
COPY server.py /sdv-pre/
COPY cli_validation.py /sdv-pre/
COPY testapi/ sdv-pre/testapi/
COPY manifest /sdv-pre/manifest/

EXPOSE 8000

CMD [ "python", "server.py" ]
