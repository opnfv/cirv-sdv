FROM python:3.8-slim-buster

WORKDIR /sdvurls/

COPY requirements.txt /state/requirements.txt
RUN pip install -r requirements.txt

COPY server /sdvurls/

CMD [ "python", "/sdvurls/server" ]
