import unittest

from rest_framework import status
from django.test import TestCase, Client

from establishments.models import (
    Establishment,
    TypeEst,
    Kitchen,
    City,
    Service,
)
from users.models import User


class EstablishmentViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        User.objects.create(
            first_name="Test_Firstname",
            last_name="Test_Lastname",
            telephone="+79108878105",
            email="TestEmail@fake.ru",
            role="restorateur",
        )
        user = User.objects.get(id=1)
        TypeEst.objects.create(name="Test Type", slug="test-type")
        Kitchen.objects.create(name="Test Kitchen", slug="test-kitchen")
        City.objects.create(name="Test City", slug="test-city")
        city = City.objects.get(id=1)
        Service.objects.create(name="Test Service", slug="test-service")
        Establishment.objects.create(
            owner=user,
            name="Test Establishment",
            cities=city,
            address="Test Address",
            latitude=1,
            longitude=1,
            average_check="до 1000",
            email=user.email,
            telephone=user.telephone,
            description="Test Description",
            is_verified=True,
        )
        cls.establishment = Establishment.objects.get(id=1)

    def setUp(self):
        self.client = Client()

    def test_get_all_establishments(self):
        response = self.client.get("/api/v2/establishments/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_establishment_detail(self):
        establishment_id = 1
        response = self.client.get(
            f"/api/v2/establishments/{establishment_id}/"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)


if __name__ == "__main__":
    unittest.main()
