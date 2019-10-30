FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#ENV TZ=UTC
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY src/requirements.txt /tmp/
RUN pip install -U pip
RUN pip install -Ur /tmp/requirements.txt

RUN mkdir /src
COPY src /src
WORKDIR /src


RUN mkdir /src/mysite/settings_local/
RUN chown www-data:www-data -R /src

USER www-data

ENTRYPOINT ["./run.sh"]
