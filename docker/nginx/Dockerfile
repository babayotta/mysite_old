FROM nginx
 
RUN mkdir /code
RUN mkdir /sock
 
#ENV TZ=UTC
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
 
ADD uwsgi_params /etc/nginx/
ADD django.conf /etc/nginx/conf.d/default.conf

