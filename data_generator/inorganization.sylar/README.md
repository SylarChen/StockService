#Data Generator
This docker container runs a cron job every day to pull Chinese stock trade records from tushare.
##tushare
http://tushare.waditu.com/
#How to use it
  1. Firstly you need a postgres instance, and one with prepopulated data will be better (https://github.com/SylarChen/StockService/tree/master/postgres_init_data)
  2. pull docker image sylarchen/dg (https://hub.docker.com/r/sylarchen/dg/)
  3. docker run -d -e DB_URL='postgresql://postgres:postgres@16.187.191.136/postgres' sylarchen/dg
     
     change DB_URL to your own, and may a proxy is needed.
  4. check postgres table public.hist
