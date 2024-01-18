import requests
from django.test import TestCase
from rest_framework import status

BASE_URL = "http://80.87.109.70/api/v1/"


class ServicesGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.base_url = BASE_URL
        self.random_id = 3

    def test_unauth_get_extras(self):
        response = requests.get(
            f"{self.base_url}services/",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_unauth_get_extras_id(self):
        response = requests.get(
            f"{self.base_url}services/{self.random_id}/",
        )
        assert response.status_code == status.HTTP_200_OK
