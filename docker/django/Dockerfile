FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src
COPY src/requirements.txt /tmp/

RUN pip install -U pip
RUN pip install -Ur /tmp/requirements.txt

