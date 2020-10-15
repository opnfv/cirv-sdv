FROM python:3.8-slim-buster

# create folder sdvconfig
RUN mkdir sdvconfig
# change the workdir to the newly created file
WORKDIR /sdvconfig/

# install from requirements.txt
COPY requirements.txt /sdvconfig/requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

# copy all required files/folders
COPY extrapolation/ /sdvconfig/extrapolation/
COPY mapping/ /sdvconfig/mapping/
COPY validation/ /sdvconfig/validation/
COPY server.py /sdvconfig/
COPY cli_validation.py /sdvconfig/
COPY testapi/ sdvconfig/testapi/
COPY manifest /sdvconfig/manifest/

# expose port for rest calls
EXPOSE 8000

# run the http server
CMD [ "python", "server.py" ]
