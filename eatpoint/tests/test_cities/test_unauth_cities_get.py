import unittest

from django.conf import settings
from django.test import TestCase, Client
from rest_framework import status
from tests.config_tests import BASE_URL


class CitiesGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        settings.ALLOWED_HOSTS.append("testserver")
        self.client = Client()
        self.random_id = 1

    def test_unauthorized_access_to_cities(self):
        response = self.client.get(
            f"{BASE_URL}/cities/",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_unauthorized_access_to_cities_id(self):
        response = self.client.get(
            f"{BASE_URL}/cities/{self.random_id}/",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)


if __name__ == "__main__":
    unittest.main()
