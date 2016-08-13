#add environment variable to mycontab -- crontab can't get docker ENV, using this as work around
printenv | cat - /etc/cron.d/myCrontab > /root/crontab.temp && mv /root/crontab.temp /etc/cron.d/myCrontab
#crontab file must be end of a new line
sed -i -e '$a\' /etc/cron.d/myCrontab

service cron start
while true
do
echo "check..."
sleep 10
done
