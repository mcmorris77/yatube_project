from django.test import TestCase, Client
from http import HTTPStatus

class CorePageTests(TestCase):
    """Тесты кастомных страниц"""

    def setUp(self):
        self.client = Client()

    def test_page_not_found(self):
        response = self.client.get('/nonexistent-page/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')



