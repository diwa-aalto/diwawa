# INSTALLATION SCRIPT FOR QNAP TS-219P II
# This script installs all the required python modules for DiWaWa and deploys DiWaWa using virtualenv, mysql, lighttpd and FastCGI.
# REQUIRES Optware(IPKG) to be installed and setup properly.
# The script also setups autorun for automatically starting diwawa at boot.
# Set variables here
# If a DIR variable is not set, it is not processed

# Django installation directory
HOME_DIR=
# Mysql data directory
MYSQL_DATA_DIR=
# Mysql temp directory
MYSQL_TEMP_DIR=
# Uploads directory for lighttpd
# if not set, lighttpd will default to /tmp
UPLOADS_DIR=
# Setup diwawa to start at boot
SETUP_AUTORUN=true
# Install and setup lighttpd
SETUP_LIGHTTPD=true
# Setup mysql database. Includes possible changing data and temp dir.
SETUP_MYSQL=true
###### DO NOT EDIT BELOW THIS ######
# escape variables
HOME_DIR_ES=${HOME_DIR//\//\\/}
MYSQL_DATA_DIR_ES=${MYSQL_DATA_DIR//\//\\/}
MYSQL_TEMP_DIR_ES=${MYSQL_TEMP_DIR//\//\\/}
UPLOADS_DIR_ES=${UPLOADS_DIR//\//\\/}

# Create dirs
if [ -n "$HOME_DIR" ]; then
mkdir -p $HOME_DIR
fi
if [ -n "$MYSQL_DATA_DIR" ]; then
mkdir -p  $MYSQL_DATA_DIR
fi
if [ -n "$MYSQL_TEMP_DIR" ]; then
mkdir -p $MYSQL_TEMP_DIR
fi
if [ -n "$UPLOADS_DIR" ]; then
mkdir -p $UPLOADS_DIR
fi

# install needed packages using ipkg
ipkg update
ipkg install python27 py27-setuptools gcc lighttpd gawk nano

#copy conf files
if $SETUP_LIGHTTPD; then
sed -i s/HOME_DIR/$HOME_DIR_ES/g lighttpd.conf
sed -i s/UPLOADS_DIR/$UPLOADS_DIR_ES/g lighttpd.conf
cp -f lighttpd.conf /opt/etc/lighttpd/lighttpd.conf
fi

if $SETUP_AUTORUN; then
cp -rf autorun /share/HDA_DATA/.qpkg
chmod +x /share/HDA_DATA/.qpkg/autorun/autorun.sh
sed -i s/HOME_DIR/$HOME_DIR_ES/g /share/HDA_DATA/.qpkg/autorun/autorun.sh
fi

if $SETUP_MYSQL; then
sed -i s/MYSQL_TEMP_DIR/$MYSQL_TEMP_DIR_ES/g my.cnf
cp -f my.cnf /etc/config/my.cnf
sed -i s/MYSQL_DATA_DIR/$MYSQL_DATADIR_ES/g mysqld.sh
cp -f mysqld.sh /mnt/ext/opt/mysql/mysqld.sh
fi

cp -f requirements.txt $HOME_DIR

# install virtualenv
python2.7 /opt/lib/python2.7/site-packages/easy_install.py virtualenv

# fetch Mysql for python
wget http://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.3/MySQL-python-1.2.3.tar.gz/download
tar zxvf MySQL-python-1.2.3.tar.gz
cp -f site.cfg MySQL-python-1.2.3
cp -rf MySQL-python-1.2.3 $HOME_DIR
rm -rf MySQL-python-1.2.3

# Copy DiWaWA to home dir
cp -rf ../ $HOME_DIR/diwawa
rm -rf $HOME_DIR/QNAP_INSTALL

# handle settings
#cp -f settings.py $HOME_DIR/diwawa/diwawa
nano -c $HOME_DIR/diwawa/diwawa/example_settings.py
# copy settings if user did not save the file as settings.py
if [ ! -f $HOME_DIR/diwawa/diwawa/settings.py ]; then
    cp $HOME_DIR/diwawa/diwawa/example_settings.py $HOME_DIR/diwawa/diwawa/settings.py
fi

# create links to static
ln -s $HOME_DIR/env/lib/python2.7/site-packages/django/contrib/admin/static/admin $HOME_DIR/diwawa/static/admin
ln -s /share/Projects $HOME_DIR/diwawa/static/Projects
ln -s /share/screen_images $HOME_DIR/diwawa/static/screen_images

# setup ipkg startup and fix path
cp -f Optware.sh /etc/init.d/

# Stop mysql, copy script from /mnt and start again.
if $SETUP_MYSQL; then
/etc/init.d/mysqld.sh stop
cp -f /mnt/ext/opt/mysql/mysqld.sh /etc/init.d/mysqld.sh
cp -rf /usr/local/mysql/var/* $MYSQL_DATA_DIR
/etc/init.d/mysqld.sh start

#Create database and user. Set root password.
#/mnt/ext/opt/mysql/bin/mysql -u root < init_mysql.sql
fi

# setup virtualenv
cd $HOME_DIR
/share/HDA_DATA/.qpkg/Optware/local/bin/virtualenv --no-site-packages env
source env/bin/activate
pip install -r requirements.txt
cd MySQL-python-1.2.3
python setup.py build
python setup.py install

# build database
cd ../diwawa
python manage.py syncdb
python manage.py migrate
deactivate

# cleanup
cd ..
rm -rf MySQL-python-1.2.3

if $SETUP_AUTORUN; then
# setup autorun
mount -t ext2 /dev/mtdblock5 /tmp/config
echo "#!/bin/sh" > /tmp/config/autorun.sh
echo "/share/HDA_DATA/.qpkg/autorun/autorun.sh &" >> /tmp/config/autorun.sh
umount /tmp/config
fi

if $SETUP_MYSQL; then
#restart mysql
/etc/init.d/mysql restart
fi

if $SETUP_LIGHTTPD; then
# start lighttpd
/opt/etc/init.d/S80lighttpd start
fi

if $SETUP_AUTORUN; then
# run autorun
/share/HDA_DATA/.qpkg/autorun/autorun.sh
fi


 


