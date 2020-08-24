FROM python:3.8-slim-buster

MAINTAINER Parth Yadav <parthyadav3105@gmail.com>

WORKDIR /server/

COPY resource-estimation/requirements.txt /server/requirements.txt
RUN pip install -r requirements.txt

COPY website/ /website/
COPY resource-estimation/ /server/

RUN rm requirements.txt

CMD [ "python", "/server/server" ]
