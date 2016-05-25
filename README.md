django-datacollect
===

simple interface for collaborative collection of data records.

Requirements
==

This django project used some django packages:
 * Django Flat Theme
 * Django Countries - https://github.com/SmileyChris/django-countries
 * Django Select Multiple Field - https://github.com/kelvinwong-ca/django-select-multiple-field
 
Create a virtual environment:
```
virtualenv django-datacollect
```

Install packages using
```
pip install django django-flat-theme django-countries django-select-multiple-field django-bootstrap3 mysql-python
```

MySQL-Pyton requires
```
sudo apt-get install libmysqlclient-dev python-mysqldb
```


Development server
==

Activate virtual environment and start dev server
```
cd django-datacollect
. bin/activate
cd datacollect

python manage.py migrate

python manage.py runserver
```