from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from AdminApp.Views import errorCode
from AdminApp.Views.room_view import insertRoom
from AdminApp.Views.workstation_view import insertWorkstation
from AdminApp.Views.user_view import insertUser


class TestViewBase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        # workstation
        self.workstation_list_url = reverse('workstationList')
        self.workstation_delete_url = reverse('workstationDelete', args=[1])
        self.workstation_insert_url = reverse('workstationInsert')
        self.workstation_modify_url = reverse('workstationModify')
        self.workstation_getinfo_url = reverse('workstationInfo')
        self.workstation_sanitize_url = reverse('workstationSanitize')
        # room
        self.room_insert_url = reverse('roomInsert')
        self.room_delete_url = reverse('roomDelete', args=[1])
        self.room_modify_url = reverse('roomModify')
        self.room_list_url = reverse('roomList')
        # user
        self.user_insert_url = reverse('userInsert')
        self.user_delete_url = reverse('userDelete', args=[1])
        self.user_modify_url = reverse('userModify')
        self.user_list_url = reverse('userList')
        self.user_login_url = reverse('login')
        self.user_bookings_url = reverse('userBookings', args=[1])

    def insertDefaultRoom(self, json):
        defRoom = self.factory.post(self.room_insert_url, json, format='json')
        res = insertRoom(defRoom)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.ROOM_THING + errorCode.OK)

    def insertDefaultWorkstation(self, json):
        defWorkstation = self.factory.post(self.workstation_insert_url, json, format='json')
        res = insertWorkstation(defWorkstation)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.WORK_THING + errorCode.OK)

    def insertDefaultUser(self, json):
        defUser = self.factory.post(self.user_insert_url, json, format='json')
        res = insertUser(defUser)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.OK)
