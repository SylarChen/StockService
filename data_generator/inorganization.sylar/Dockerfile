FROM ubuntu
MAINTAINER Sylar Chen

#ENV http_proxy 'http://web-proxy.atl.hp.com:8080'
#ENV https_proxy 'http://web-proxy.atl.hp.com:8080'

RUN apt-get update && apt-get upgrade -y && \
apt-get install -y vim && \
apt-get install -y python3 python3-dev gcc libpq-dev python3-lxml python3-pandas python3-pip && \
apt-get clean

#build up python dependency
#RUN pip3 --proxy http://web-proxy.atl.hp.com:8080 install tushare psycopg2 threadpool sqlalchemy
RUN pip3 install tushare psycopg2 threadpool sqlalchemy

#copy my source code to image
RUN mkdir -p /DG
ADD db_config.py /DG/
ADD data_generator.py /DG/
ADD always-start.sh /DG/
RUN chmod +x /DG/always-start.sh

#set DB url
#ENV DB_URL 'postgresql://postgres:postgres@16.187.191.136/postgres'
ENV DB_URL 'postgresql://postgres:postgres@127.0.0.1/postgres'

ENTRYPOINT ["/bin/bash","/DG/always-start.sh"]
