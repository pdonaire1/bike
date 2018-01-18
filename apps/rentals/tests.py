from django.test import TestCase
from rentals.models import Rental, RentalType, BikeRental, Promotion
from bikes.models import Bike
from clients.models import Client
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User

class RentalModelTests(TestCase):

    def setUp(self):
        self.rental_client = Client.objects.create(
            full_name='John Due',
            phone='04241231231',
            address='New York')
        self.bike_electric = Bike.objects.create(
            bike_code='001',
            bike_type=Bike.ELECTRIC)
        self.bike_travel = Bike.objects.create(
            bike_code='002',
            bike_type=Bike.TRAVEL)
        self.bike_road = Bike.objects.create(
            bike_code='003',
            bike_type=Bike.ROAD)
        self.bike_mountain = Bike.objects.create(
            bike_code='004',
            bike_type=Bike.MOUNTAIN)

        self.rental_type = RentalType.objects.create(amount=5, length="hour")

        self.user_password = 'temporary'
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', self.user_password)

    def test_simple_bike_rental_created(self):
        """
        Test for make a valid Rental object with one bike rented
        """
        self.rental = Rental.objects.create(client=self.rental_client)
        self.bike_rental = BikeRental.objects.create(
            bike=self.bike_electric,
            rental=self.rental,
            rental_type=self.rental_type
        )

        self.assertIs(BikeRental.objects.filter(
            rental=self.rental,
            rental_type=self.rental_type,
            bike=self.bike_electric).exists(), True)
        self.assertIs(Rental.objects.filter(client=self.rental_client).exists(), True)
        self.assertEqual(self.rental.total_amount, '5.0$')
        self.assertEqual(self.rental.due, '5.0$')

    def test_bikes_rental_created(self):
        """
        Test to make a valid Rental object with severals bikes rented
        """
        self.rental = Rental.objects.create(client=self.rental_client)
        bikes_types = [self.bike_electric, self.bike_travel, self.bike_road, self.bike_mountain]
        for bike in bikes_types:
            self.bike_rental = BikeRental.objects.create(
                bike=bike,
                rental=self.rental,
                rental_type=self.rental_type
            )
        # New Query to make sure we have the correct amount and records
        bike_rental_count = BikeRental.objects.filter(rental=self.rental).count()
        total_amount = float(self.rental_type.amount * bike_rental_count)
        self.assertIs(BikeRental.objects.filter(
            rental=self.rental,
            rental_type=self.rental_type,
            bike=self.bike_electric).exists(), True)
        self.assertIs(Rental.objects.filter(client=self.rental_client).exists(), True)
        self.assertEqual(self.rental.total_amount, str(total_amount)+'$')
        self.assertEqual(self.rental.due, '20.0$')

        self.rental.finished = True
        self.rental.save()
        self.assertEqual(self.rental.total_amount, '20.0$')
        self.assertEqual(self.rental.due, '0$')


class RentalsViewTests(TestCase):

    def setUp(self):
        self.rental_client = Client.objects.create(
            full_name='John Due',
            phone='04241231231',
            address='New York')
        self.bike_electric = Bike.objects.create(
            bike_code='001',
            bike_type=Bike.ELECTRIC)
        self.bike_travel = Bike.objects.create(
            bike_code='002',
            bike_type=Bike.TRAVEL)
        self.bike_road = Bike.objects.create(
            bike_code='003',
            bike_type=Bike.ROAD)
        self.bike_mountain = Bike.objects.create(
            bike_code='004',
            bike_type=Bike.MOUNTAIN)
        self.rental_type = RentalType.objects.create(amount=5, length="hour")

        self.user_password = 'temporary'
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', self.user_password)

    def test_detail_rentals(self):
        """
        The detail view of a rental
        """
        self.rental = Rental.objects.create(client=self.rental_client)
        self.bike_rental = BikeRental.objects.create(
            bike=self.bike_electric,
            rental=self.rental,
            rental_type=self.rental_type
        )

        url = reverse('rental-detail', kwargs={'pk': self.rental.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.rental.client.full_name)
        self.assertContains(response, self.rental.client.address)
        self.assertEqual(len(response.context['bike_rentals']), 1)
        self.assertEqual(response.context['bike_rentals'][0].id, self.bike_rental.id)
        self.assertEqual(response.context['object'], self.rental)
        self.assertEqual(
            response.context['object'].total_amount,
            str(float(self.rental_type.amount)) + '$')

    def test_index_rentals(self):
        """
        The index or list of rentals
        """
        self.rental = Rental.objects.create(client=self.rental_client)

        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.rental.client.full_name)
        self.assertContains(response, self.rental.client.phone)
        self.assertEqual(len(response.context['rentals']), 1)
        self.assertEqual(response.context['rentals'][0].id, self.rental.id)
        self.rental.finished = True
        self.rental.save()
        rental = Rental.objects.create(client=self.rental_client)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rentals']), 2)
        self.assertEqual(response.context['rentals'][0].id, self.rental.id)
        self.assertEqual(response.context['rentals'][1].id, rental.id)

    def test_create_rental(self):
        """
        Test for create rental, to make sure rental was successfully created
        """
        self.rental = Rental.objects.create(client=self.rental_client)

        url = reverse('new-rental')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        params = {
            'phone': '12345678901',
            'full_name': 'Marty McFly',
            'address': '1600 S Azusa Ave',
            'bike_code-0': self.bike_electric.id,
            'rental_types-0': self.rental_type.id
        }
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.post(url, data={}, follow=True)
        for m in response.context['messages']:
            self.assertEqual(str(m), 'Error: you have to fill all fields')
            break
        response = self.client.post(url, data=params, follow=True)
        self.assertEqual(response.status_code, 200)
        for m in response.context['messages']:
            self.assertEqual(str(m), 'Rental Successfully Created')
            break
        #Let's proof that object was created successfully
        rental = Rental.objects.all().last()
        self.assertEqual(rental.client.full_name, params['full_name'])
        self.assertEqual(rental.client.phone, params['phone'])
        self.assertEqual(rental.client.address, params['address'])
        bike_rentals = BikeRental.objects.all()
        self.assertEqual(bike_rentals.count(), 1)
        self.assertEqual(
            rental.total_amount,
            str(float(self.rental_type.amount)) + '$')

    def test_create_rental(self):
        """
        Test for create rental, to make sure rental was successfully created
        with the promotion
        """
        self.rental = Rental.objects.create(client=self.rental_client)
        promotion = Promotion.objects.create(
            count_rental_to=5,
            count_rental_from=3,
            percentaje_discount=30,
            name='Family Rent')
        url = reverse('new-rental')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        params = {
            'phone': '12345678901',
            'full_name': 'Marty McFly',
            'address': '1600 S Azusa Ave',
            'bike_code-0': self.bike_electric.id,
            'rental_types-0': self.rental_type.id,
            'bike_code-1': self.bike_travel.id,
            'rental_types-1': self.rental_type.id,
            'bike_code-2': self.bike_road.id,
            'rental_types-2': self.rental_type.id,
            'bike_code-3': self.bike_mountain.id,
            'rental_types-3': self.rental_type.id
        }
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.post(url, data={}, follow=True)
        for m in response.context['messages']:
            self.assertEqual(str(m), 'Error: you have to fill all fields')
            break
        response = self.client.post(url, data=params, follow=True)
        self.assertEqual(response.status_code, 200)
        for m in response.context['messages']:
            self.assertEqual(str(m), 'Rental Successfully Created')
            break
        #Let's proof that object was created successfully
        rental = Rental.objects.all().last()
        self.assertEqual(rental.client.full_name, params['full_name'])
        self.assertEqual(rental.client.phone, params['phone'])
        self.assertEqual(rental.client.address, params['address'])
        bike_rentals = BikeRental.objects.all()
        self.assertEqual(bike_rentals.count(), 4)
        discount = float(self.rental_type.amount * 4 * promotion.percentaje_discount / 100)
        amount = float(self.rental_type.amount * 4)
        total_amount = str(amount - discount) + '$'
        self.assertEqual(rental.total_amount, total_amount)
        rental.finished = True
        rental.save()
        self.assertEqual(rental.due, str('0$'))
