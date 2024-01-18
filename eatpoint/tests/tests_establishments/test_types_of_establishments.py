import unittest
import requests
from rest_framework import status

from tests.config_tests import BASE_URL


class TypeEstablishmentsGETUnauthTests(unittest.TestCase):
    def setUp(self):
        self.base_url = BASE_URL
        self.random_id = 3

    def test_unauthorized_access_to_types(self):
        response = requests.get(f"{self.base_url}types/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_to_types_id(self):
        response = requests.get(f"{self.base_url}types/{self.random_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
