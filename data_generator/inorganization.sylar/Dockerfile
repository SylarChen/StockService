FROM ubuntu
MAINTAINER Sylar Chen

#ENV http_proxy 'http://web-proxy.atl.hp.com:8080'
#ENV https_proxy 'http://web-proxy.atl.hp.com:8080'

RUN apt-get update && apt-get upgrade -y && \
apt-get install -y vim cron && \
apt-get install -y python3 python3-dev gcc libpq-dev python3-lxml python3-pandas python3-pip && \
apt-get clean && rm -rf /var/lib/apt/lists/*

#build up python dependency
#RUN pip3 --proxy http://web-proxy.atl.hp.com:8080 install tushare psycopg2 threadpool sqlalchemy
RUN pip3 install tushare psycopg2 threadpool sqlalchemy

# change localtime
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#copy my source code to image
RUN mkdir -p /DG
ADD db_config.py /DG/
ADD data_generator.py /DG/
ADD crontab.py /DG/

#set DB url
#ENV DB_URL 'postgresql://postgres:postgres@16.187.191.136/postgres'
ENV DB_URL 'postgresql://postgres:postgres@127.0.0.1/postgres'

ADD myCrontab /etc/cron.d/
RUN touch /crontabLog

#add entrypoint
ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
