import requests
from django.test import TestCase
from rest_framework import status

BASE_URL = "http://80.87.109.70/api/v1/"


class ZonesGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.base_url = BASE_URL
        self.random_id = 2

    def test_unauthorized_access_to_zones(self):
        response = requests.get(
            f"{self.base_url}establishments/{self.random_id}/zones/",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_unauthorized_access_to_zones_id(self):
        response = requests.get(
            self.base_url
            + f"establishments/{self.random_id}/zones/{self.random_id}/",
        )
        assert response.status_code == status.HTTP_200_OK
