FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#ENV TZ=UTC
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /src
WORKDIR /src
COPY src /src
COPY src/requirements.txt /tmp/

RUN pip install -U pip
RUN pip install -Ur /tmp/requirements.txt

ENTRYPOINT ["./run.sh"]
