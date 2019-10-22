FROM python:3

ENV PYTHONUNBUFFERED 1

COPY src/requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /src/
WORKDIR /src/
COPY src/ /src/
