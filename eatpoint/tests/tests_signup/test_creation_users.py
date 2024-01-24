from django.test import TestCase, Client
from rest_framework import status
from tests.config_tests import BASE_URL
import random


class SignUpTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        """
        Устанавливает тестовое окружение,
        инициализируя базовый URL и создавая тестовые данные пользователя.
        """
        self.client = Client()
        self.user_data = {
            "telephone": "+79108878111",
            "email": "user"
            + "".join(random.choices("0123456789", k=10))
            + "@example.com",
            "first_name": "firstname"
            + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
            "last_name": "lastname"
            + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
            "role": "client",
            "password": "!SOMEinterestpassword",
            "is_agreement": True,
            "confirm_code_send_method": "nothing",
        }

    def test_user_creation_role_client(self):
        response = self.client.post(
            f"{BASE_URL}/auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_role_establishment(self):
        self.user_data["role"] = "restorateur"
        response = self.client.post(
            f"{BASE_URL}/auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_with_wrong_role(self):
        self.user_data["role"] = "admin"
        response = self.client.post(
            f"{BASE_URL}/auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_with_wrong_email(self):
        self.user_data["email"] = "wrong_email@"
        response = self.client.post(
            f"{BASE_URL}/auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_with_wrong_phone(self):
        self.user_data["telephone"] = "89999999999"
        response = self.client.post(
            f"{BASE_URL}/auth/signup/",
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
