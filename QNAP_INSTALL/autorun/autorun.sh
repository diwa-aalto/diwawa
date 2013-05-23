#!/bin/sh
# Optware manual fix
rm -rf /opt
ln -sf /share/HDA_DATA/.qpkg/Optware /opt
/share/HDA_DATA/.qpkg/Optware/Optware.sh start
sleep 60
/etc/init.d/mysqld.sh stop
cp -f /mnt/ext/opt/mysql/mysqld.sh /etc/init.d/mysqld.sh
/etc/init.d/mysqld.sh start
/mnt/ext/opt/mysql/bin/mysqladmin -u root -padmin status
HOME_DIR/env/bin/python HOME_DIR/diwawa/manage.py runfcgi method=threaded host=127.0.0.1 port=3033
