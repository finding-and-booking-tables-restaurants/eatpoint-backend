import unittest
from django.test import TestCase, Client
from rest_framework import status

from tests.config_tests import BASE_URL


class ReservationsGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.client = Client()
        self.random_id = 1

    def test_unauthorized_access_to_reservations(self):
        response = self.client.get(f"{BASE_URL}/reservations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main()
