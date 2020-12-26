# in case we ever do any installs
# lets make them non-interactive
ARG DEBIAN_FRONTEND=noninteractive

###### stage 1 - build image with dependencies
#python image as base
FROM python:3.8.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /external

VOLUME /external

COPY Docker_Access.py ./

#CMD [ "python", "./Access.py",  "dgreen8443", "dgreen8443", "d4671af90b713d32019f549dfcf447d1a80465f3"]



