#/bin/bash!

for server in $(seq 4 50);do
   scp -P17717 ./userdict/userdict 192.168.241.$server:/usr/lib/python2.7/site-packages/jieba/userdict/
done
