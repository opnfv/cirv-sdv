FROM python:3.8-slim-buster

# create folder config
RUN mkdir config
# change the workdir to the newly created file
WORKDIR /config/

# install from requirements.txt
COPY requirements.txt /config/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

# copy all required files/folders
COPY extrapolation/ /config/extrapolation/
COPY mapping/ /config/mapping/
COPY validation/ /config/validation/
COPY server.py /config/
COPY cli_validation.py /config/
COPY testapi/ config/testapi/
COPY manifest /config/manifest/

# expose port for rest calls
EXPOSE 8000

# run the http server
CMD [ "python", "server.py" ]
