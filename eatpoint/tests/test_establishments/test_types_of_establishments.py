import unittest
from django.test import TestCase, Client
from rest_framework import status

from tests.config_tests import BASE_URL


class TypeEstablishmentsGETUnauthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.random_id = 1

    def test_unauthorized_access_to_types(self):
        response = self.client.get(f"{BASE_URL}/types/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_unauthorized_access_to_types_id(self):
        response = self.client.get(f"{BASE_URL}/types/{self.random_id}/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


if __name__ == "__main__":
    unittest.main()
