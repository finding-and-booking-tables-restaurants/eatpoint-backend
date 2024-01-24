import unittest
from django.test import TestCase, Client
from rest_framework import status
from tests.config_tests import BASE_URL


class ServicesGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.client = Client()
        self.random_id = 1

    def test_unauth_get_extras(self):
        response = self.client.get(
            f"{BASE_URL}/services/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauth_get_extras_id(self):
        response = self.client.get(
            f"{BASE_URL}/services/{self.random_id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
