from django.test import TestCase
from rentals.models import Rental, RentalType, BikeRental
from bikes.models import Bike
from clients.models import Client
from django.core.urlresolvers import reverse, reverse_lazy

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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.rental.client.full_name)
        self.assertContains(response, self.rental.client.address)
        self.assertEqual(len(response.context['bike_rentals']), 1)
        self.assertEqual(response.context['bike_rentals'][0].id, self.bike_rental.id)
        self.assertEqual(response.context['object'], self.rental)

    def test_index_rentals(self):
        """
        The index or list of rentals
        """
        self.rental = Rental.objects.create(client=self.rental_client)
        # self.bike_rental = BikeRental.objects.create(
        #     bike=self.bike_electric,
        #     rental=self.rental,
        #     rental_type=self.rental_type
        # )

        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.rental.client.full_name)
        self.assertContains(response, self.rental.client.phone)
        self.assertEqual(len(response.context['rentals']), 1)
        self.assertEqual(response.context['rentals'][0].id, self.rental.id)
