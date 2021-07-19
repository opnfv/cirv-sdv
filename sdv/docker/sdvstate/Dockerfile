FROM python:3.8-slim-buster

MAINTAINER Parth Yadav <parthyadav3105@gmail.com>

WORKDIR /sdv/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY internal/ internal/
COPY settings/ settings/
COPY tools/ tools/
COPY state .
COPY server .

ENV RESULTS_PATH /tmp/
ENV RESULTS_FILENAME results.json
ENV LOG_VERBOSITY info
ENV SAVE_RESULTS_LOCALLY True

WORKDIR /data/

CMD [ "python", "/state/server" ]
