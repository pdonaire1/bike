# Created by: @pdonaire1

# Running enviroment
1. Creating Python's enviroment
```
mkvirtualenv bike_vrt
pip install -r requirements.txt
pip install unipath
```

Configure database's credentials in DATABASES in `bike_api/settings.py` and run:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata apps/base/fixtures/constants.json
python manage.py loaddata apps/base/fixtures/bikes.json
python manage.py runserver
```

Go to the page: http://127.0.0.1:8000/

# Running tests
Located in apps/rentals/tests.py
```
python manage.py test apps/rentals
```

# DataBase Graph
![alt text](https://github.com/pdonaire1/bike/blob/master/Diagrama1.png)

# Explanation:
Bike is an app to rent bikes of differents types.
1. The user of system will add new rentals and then he can view all rentals history in the index of the plattform
2. In index the user has all rentals with information, to get the invoice of the rental, user can click the "i" icon to get more information.
3. If the rental was not delivered by the client, it will appear a button to finish the rental that's mean that client has delivered the bikes.
4. In index also exists the action delete, by clicking on a comfirmation screen appear.
