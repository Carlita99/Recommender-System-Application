FROM python:alpine3.6

ENV PYTHONUNBUFFERED 1
ENV APOC_VERSION 3.5.0.1
ENV APOC_URI https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/${APOC_VERSION}/apoc-${APOC_VERSION}-all.jar

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache bash gawk sed grep bc coreutils build-base gcc libffi-dev python-dev openssl-dev
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
