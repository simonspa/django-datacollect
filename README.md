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
 * Django Reversion for version control - https://github.com/etianen/django-reversion/
 * GeoPy geocoder - https://github.com/geopy/geopy
 * Django GeoJSON for storing geoJSON objects in the regular database - https://github.com/makinacorpus/django-geojson
 * Django JSONField for the PointField of geoJSON - https://github.com/bradjasper/django-jsonfield
 
Create a virtual environment:
```
virtualenv django-datacollect
```

Install packages using
```
pip install django django-flat-theme django-countries django-select-multiple-field django-bootstrap3 mysql-python django-reversion django-leaflet django-geojson django-jsonfield geopy django-mathfilters
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