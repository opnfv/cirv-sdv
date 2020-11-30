======================
SDVConfig Config Guide
======================
Welcome to the SDVConfig config Guide!

Who should use this guide?

If you are searching for a way to run the sdvconfig code and don't know how, this guide is for you.

There currently exists two ways of running the code, they are through commandline and through docker-http.

Commandline
^^^^^^^^^^^
The configuration required are as follows.

Use Python Virtual Environment Manager
```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```
Install the required packages from requirements.txt

```
pip install -r requirements.txt
```
Please refer the user guide on how to run the code on commandline.

docker-http
^^^^^^^^^^^
Make sure you have docker installed before proceeding any further.

The Dockerfile contents are as follows.

.. code:: bash
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

Build the docker image with the following command.

```
docker build --tag <user>/sdvconfig:<version>
```
You’ll see Docker step through each instruction in your Dockerfile, building up your image as it goes. If successful, the build process should end with a message Successfully tagged <user>/sdvconfig:<version>.

Finally we can run the image as a container with the follwing command.

```
docker run -v /path/to/folder:/path/to/folder --publish 8000:8000 --detach --name config <user>/sdvconfig:<version>
```

There are a couple of common flags here:
-  --publish asks Docker to forward traffic incoming on the host’s port 8000 to the container’s port 8080. Containers have their own private set of ports, so if you want to reach one from the network, you have to forward traffic to it in this way. Otherwise, firewall rules will prevent all network traffic from reaching your container, as a default security posture.
- --detach asks Docker to run this container in the      background.
- --name specifies a name with which you can refer to your container in subsequent commands, in this case config.
Finally we attach a volume from the localhost to the container so we can feed in files such as pdf, manifests to docker-http module and get the results persisted in this volume . This is done with ``` -v ```.

Please refer the user guide regarding the http requests.

