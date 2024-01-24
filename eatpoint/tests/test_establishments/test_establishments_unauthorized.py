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
from reviews.models import Review
from users.models import User
from tests.config_tests import BASE_URL


class EstablishmentViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create(
            first_name="Test_Firstname",
            last_name="Test_Lastname",
            telephone="+79108878106",
            email="TestEmail@fake.ru",
            role="restorateur",
        )
        user = User.objects.get(id=1)
        TypeEst.objects.get_or_create(name="Test Type", slug="test-type")
        Kitchen.objects.get_or_create(name="Test Kitchen", slug="test-kitchen")
        City.objects.get_or_create(name="Test City", slug="test-city")
        city = City.objects.get(id=1)
        Service.objects.get_or_create(name="Test Service", slug="test-service")
        Establishment.objects.get_or_create(
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
        establishment = Establishment.objects.get(id=1)
        Review.objects.get_or_create(
            establishment=establishment,
            author=user,
            text="Test Text",
            score=5,
        )

    def setUp(self):
        self.client = Client()

    def test_get_all_establishments(self):
        response = self.client.get(f"{BASE_URL}/establishments/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_establishment_detail(self):
        establishment_id = 1
        response = self.client.get(
            f"{BASE_URL}/establishments/{establishment_id}/"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)


if __name__ == "__main__":
    unittest.main()
