import requests
from django.test import TestCase
from rest_framework import status
import random


BASE_URL = "http://80.87.109.70/api/v1/"


class SignUpTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.base_url = BASE_URL
        self.user_data = {
            "telephone": "+7" + "".join(random.choices("0123456789", k=10)),
            "email": "user"
            + "".join(random.choices("0123456789", k=10))
            + "@example.com",
            "first_name": "firstname"
            + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
            "last_name": "lastname"
            + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
            "role": "client",
            "password": "someinterestpassword",
            "is_agreement": True,
            "confirm_code_send_method": "nothing",
        }

    def test_user_creation_role_client(self):
        response = requests.post(
            f"{self.base_url}auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # TODO: 201

    def test_user_creation_role_establishment(self):
        self.user_data["role"] = "restorateur"
        response = requests.post(
            f"{self.base_url}auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # TODO: 201

    def test_user_creation_with_wrong_role(self):
        self.user_data["role"] = "admin"
        response = requests.post(
            f"{self.base_url}auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_with_wrong_email(self):
        self.user_data["email"] = "wrong_email@"
        response = requests.post(
            f"{self.base_url}auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_with_wrong_phone(self):
        self.user_data["telephone"] = "89999999999"
        response = requests.post(
            f"{self.base_url}auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
