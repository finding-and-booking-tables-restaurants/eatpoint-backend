import unittest
from django.test import TestCase, Client
from rest_framework import status
from tests.config_tests import BASE_URL


class ReviewGETUnauthTests(TestCase):
    """
    Базовое тестирование эндпоинтов.
    """

    def setUp(self):
        self.client = Client()
        self.random_id = 1

    def test_unauthorized_access_to_reviews(self):
        response = self.client.get(
            f"{BASE_URL}/establishments/{self.random_id}/reviews/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_to_reviews_id(self):
        response = self.client.get(
            f"{BASE_URL}/establishments/{self.random_id}/reviews/{self.random_id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
