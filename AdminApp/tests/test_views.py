from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from AdminApp.views import insertWorkstation


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        self.list_url = reverse('list')
        self.delete_url = reverse('delete', args=[1])
        self.insert_url = reverse('insert')


    def test_getWorkstations_GET(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_insertWorkstation_POST(self):
        request = self.factory.post(self.insert_url, {'WorkstationId': '1', 'Xposition': '0', 'Yposition': '0', 'Status': 'status' }, format='json')
        response = insertWorkstation(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), '"Added Successfully!!"')