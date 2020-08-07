FROM python:3.8-slim-buster

MAINTAINER Parth Yadav <parthyadav3105@gmail.com>

WORKDIR /state/

COPY requirements.txt /state/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY core/ /state/core/
COPY settings/ /state/settings/
COPY tools/ /state/tools/
COPY validator/ /state/validator/
COPY state /state/
COPY server /state/

ENV RESULTS_PATH /tmp/
ENV RESULTS_FILENAME results.json
ENV LOG_VERBOSITY info
ENV SAVE_RESULTS_LOCALLY True

WORKDIR /data/

CMD [ "python", "/state/server" ]
