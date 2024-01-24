from django.test import TestCase, Client
from rest_framework import status
from tests.config_tests import BASE_URL


class ZonesGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.client = Client()
        self.random_id = 1

    def test_unauthorized_access_to_zones(self):
        response = self.client.get(
            f"{BASE_URL}/establishments/{self.random_id}/zones/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_to_zones_id(self):
        response = self.client.get(
            f"{BASE_URL}/establishments/{self.random_id}/zones/{self.random_id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
