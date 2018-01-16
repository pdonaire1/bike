# Created by: @pdonaire1

Cada bicicleta tiene su codigo,
cuando se cera una renta se crea a traves del client, se verifica si ya es usuario,
si no lo es se llenan los datos a mano.

Si va a rentar mas de una bicicleta entonces se crea un formulario dinamico
pero el cliente va a ser siempre el mismo

formulario de ejemplo:

phone: ________
full_name: ____
address: ______
------------------
bike: [(1,'bikeone'), (2,'biketwo'), (3,'bikethree' #SELECTED)]
rental_type: [(1,'5 per hour'), (2,'20 per day'), (3,'60 per month')]
(add another button)
bike: [(1,'bikeone'), (2,'biketwo')]
rental_type: [(1,'5 per hour'), (2,'20 per day'), (3,'60 per month')]

MAS ABAJO
Filtro de bicicletas disponibles
------------------
code | bike_type (al darle click a alguna se selecciona en el formulario)
001   mountain
002   mountain
003   road

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
