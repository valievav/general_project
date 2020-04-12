FROM python:3.8-alpine
MAINTAINER Venus

# to see Python logs in real time w/o buffering
ENV PYTHONUNBUFFERED 1

# install requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create working directory for app
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# workaround to be able to mount volume as non-root user https://github.com/moby/moby/issues/2259
RUN chown -R $(whoami):$(whoami) /app
RUN export UID=${UID} && export GID=${GID}

# create user to run app on Docker (for security, in case root user is compromised)
RUN adduser -D venus_docker
USER venus_docker
