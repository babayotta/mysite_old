FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#ENV TZ=UTC
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /src
COPY src /src
WORKDIR /src

RUN pip install -U pip
RUN pip install -Ur requirements.txt

ENTRYPOINT ["./run.sh"]
