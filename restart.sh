kill -9 `pidof python`
/share/HDA_DATA/homes/django/env/bin/python /share/HDA_DATA/homes/django/diwawa/manage.py runfcgi host=127.0.0.1 port=3033 method=threaded