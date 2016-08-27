#add environment variable to mycontab -- crontab can't get docker ENV, using this as work around
printenv | cat - /etc/cron.d/myCrontab > /root/crontab.temp && mv /root/crontab.temp /etc/cron.d/myCrontab
#crontab file must be end of a new line
sed -i -e '$a\' /etc/cron.d/myCrontab
#start cron service
service cron start
#using this loop to make container live
while true
do
echo "check..."
sleep 100
done
