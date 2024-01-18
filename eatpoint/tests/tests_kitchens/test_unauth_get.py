import requests
from django.test import TestCase
from rest_framework import status

BASE_URL = "http://80.87.109.70/api/v1/"


class KitchensGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.base_url = BASE_URL
        self.random_id = 3

    def test_unauthorized_acces_to_kitchens(self):
        response = requests.get(
            f"{self.base_url}kitchens/",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_unauthorized_acces_to_kitchens_id(self):
        response = requests.get(
            f"{self.base_url}kitchens/{self.random_id}/",
        )
        assert response.status_code == status.HTTP_200_OK
