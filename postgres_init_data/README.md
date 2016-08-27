#Postgres Data Dump
hist.zip is postgres data dump which contains records of Chinese stock trade market from 1990 to 2016.07

#How to use it
  1. install git lfs:

  https://git-lfs.github.com/

  https://github.com/github/git-lfs/issues/994
  2. run command "git lfs pull" to get hist.zip
  3. unzip hist.zip, then you'll get hist.sql
  4. run command "psql -f ./hist.sql" to populate data to your postgres
  5. check postgres table public.hist
  
#With Docker
docker run -d -p 5435:5432 --name mypostgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -v {$host_dir}:/docker-entrypoint-initdb.d postgres

{$host_dir} contains hist.sql, then postgres container will auto populate it.
