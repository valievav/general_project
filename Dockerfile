FROM python:3.8-alpine
MAINTAINER Venus

# to see Python logs in real time w/o buffering
ENV PYTHONUNBUFFERED 1

# install requirements
COPY ./requirements.txt /requirements.txt
# install postgresql-client with alpine (--no-cache for faster Docker build)
RUN apk add --update --no-cache postgresql-client
# install temp dependencies (for psycopg2)
RUN apk add --update --no-cache --virtual .temp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# remove temp dependencies after psycopg2 installed
RUN apk del .temp-build-deps

# create working directory for app
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# workaround to mount volume as non-root user https://github.com/moby/moby/issues/2259
RUN chown -R $(whoami):$(whoami) /app
RUN export UID=${UID} && export GID=${GID}

# create user to run app on Docker (for security, in case root user is compromised)
RUN adduser -D docker_user
USER docker_user
