import unittest
from django.test import TestCase, Client
from rest_framework import status
from tests.config_tests import BASE_URL
from django.conf import settings


class KitchensGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.client = Client()
        self.random_id = 1
        settings.ALLOWED_HOSTS.append("testserver")

    def test_unauthorized_access_to_kitchens(self):
        response = self.client.get(f"{BASE_URL}/kitchens/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_to_kitchens_id(self):
        response = self.client.get(f"{BASE_URL}/kitchens/{self.random_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
