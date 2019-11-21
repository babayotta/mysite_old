FROM nginx
 
#ENV TZ=UTC
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
 
ADD uwsgi_params /etc/nginx/
ADD django.conf /etc/nginx/conf.d/default.conf
ADD babayotta.su-EncryptionEverywhere-DigiCertGlobalRoot.crt /etc/ssl/
ADD babayotta.su.key /etc/ssl/
