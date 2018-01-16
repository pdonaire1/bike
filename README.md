# Created by: @pdonaire1

# Running enviroment
1. Creating Python's enviroment
```
mkvirtualenv bike_vrt
pip install -r requirements.txt
```

Configure database's credentials in DATABASES in `bike_api/settings.py` and run:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata apps/base/fixtures/constants.json
python manage.py runserver
```

Go to the page: http://127.0.0.1:8000/
