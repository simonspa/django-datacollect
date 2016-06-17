django-datacollect
===

simple interface for collaborative collection of data records.

Requirements
==

This django project used some django packages:
 * Django Flat Theme
 * Django Countries - https://github.com/SmileyChris/django-countries
 * Django Select Multiple Field - https://github.com/kelvinwong-ca/django-select-multiple-field
 * Django Leaflet for map views - https://github.com/makinacorpus/django-leaflet
 * Django Reversion forversion control - https://github.com/etianen/django-reversion/
 
Create a virtual environment:
```
virtualenv django-datacollect
```

Install packages using
```
pip install django django-flat-theme django-countries django-select-multiple-field django-bootstrap3 mysql-python django-reversion django-leaflet
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