from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from AdminApp.Views.errorCode import insertWorkstation, deleteWorkstation


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
        requestSucess = self.factory.post(self.insert_url, {'WorkstationId': '1', 'Xposition': '0', 'Yposition': '0', 'Status': 'status' }, format='json')
        requestFail = self.factory.post(self.insert_url, {'WorkstationId': '1', 'Xposition': '0', 'Yposition': '0', 'Status': 'status' }, format='json')
        responseS = insertWorkstation(requestSucess)  # insert first time, no big deal
        self.assertEqual(responseS.status_code, 200)
        self.assertEqual(responseS.content.decode("utf-8"), '"Added Successfully!!"')
        responseF = insertWorkstation(requestFail)  # insert second time, its an error cause there is already one
        self.assertEqual(responseF.status_code, 200)
        self.assertEqual(responseF.content.decode("utf-8"), '"Failed to Add."')

    def test_insertWorkstatuion_GET(self):
        response = self.client.get(self.insert_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), '"Wrong request method, required POST"')

    def test_deleteWorkstation_NoObj_GET(self):
        request = self.factory.get(self.delete_url)
        response = deleteWorkstation(request, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), '"No object found"')

    def test_deleteWorkstation_GET(self):
        requestSucess = self.factory.post(self.insert_url, {'WorkstationId': '1', 'Xposition': '0', 'Yposition': '0',
                                                            'Status': 'status'}, format='json')
        insertWorkstation(requestSucess)  # insert a new workstation
        request = self.factory.get(self.delete_url)
        response = deleteWorkstation(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), '"Deleted Successfully!!"')

