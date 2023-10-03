# Тесты

from http import HTTPStatus
from django.test import Client, TestCase

class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """тестовый тест для проверки работы workflow"""
        "в дальнейшем это можно удалить"
        
        status_code = 200
        self.assertEqual(status_code, HTTPStatus.OK)
