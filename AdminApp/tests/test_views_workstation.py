from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from AdminApp.Views.workstation_view import insertWorkstation, deleteWorkstation
from AdminApp.Views.room_view import insertRoom


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        self.workstation_list_url = reverse('workstationList')
        self.workstation_delete_url = reverse('workstationDelete', args=[1])
        self.workstation_insert_url = reverse('workstationInsert')
        self.room_insert = reverse('roomInsert')


    def test_insertWorkstation_POST(self):
        requestSucess = self.factory.post(self.workstation_insert_url,
                                          {'id': 1, 'tag': 'aa aa aa aa aa', 'workstationname': 'testname',
                                           'xworkstation': 0, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                           'sanitized': 0, 'archived': 0}, format='json')
        requestFail = self.factory.post(self.workstation_insert_url,
                                        {'id': 1, 'tag': 'aa aa aa aa aa', 'workstationname': 'testname',
                                         'xworkstation': 0, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                         'sanitized': 0, 'archived': 0}, format='json')
        responseS = insertWorkstation(requestSucess)  # insert first time, no big deal
        self.assertEqual(responseS.status_code, 200)
        self.assertEqual(responseS.content.decode("utf-8"), '"Added Successfully!!"')
        responseF = insertWorkstation(requestFail)  # insert second time, its an error cause there is already one
        self.assertEqual(responseF.status_code, 200)
        self.assertEqual(responseF.content.decode("utf-8"), '"Failed to Add."')

    def test_insertWorkstatuion_GET(self):
        response = self.client.get(self.workstation_insert_url)
        self.assertEqual(response.status_code, 405)

    def test_getWorkstations_GET(self):
        response = self.client.get(self.workstation_list_url)
        self.assertEqual(response.status_code, 200)

    def test_deleteWorkstation_NoObj_GET(self):
        request = self.factory.get(self.workstation_delete_url)
        response = deleteWorkstation(request, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), '"No object found"')

    def test_deleteWorkstation_GET(self):
        requestSucess = self.factory.post(self.workstation_insert_url,
                                          {'WorkstationId': '1', 'Xposition': '0', 'Yposition': '0',
                                           'Status': 'status'}, format='json')
        insertWorkstation(requestSucess)  # insert a new workstation
        request = self.factory.get(self.workstation_delete_url)
        response = deleteWorkstation(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), '"Deleted Successfully!!"')
