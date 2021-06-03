from django.test import SimpleTestCase
from django.urls import reverse, resolve
from AdminApp.Views.room_view import getRooms, insertRoom, deleteRoom, modifyRoom

class TestUrlsRoom(SimpleTestCase):

    def test_url_getroom(self):
        url = reverse('roomList')
        self.assertEqual(resolve(url).func, getRooms)

    def test_url_insertroom(self):
        url = reverse('roomInsert')
        self.assertEqual(resolve(url).func, insertRoom)

    def test_url_deleteroom(self):
        url = reverse('roomDelete', args=[1])
        self.assertEqual(resolve(url).func, deleteRoom)

    def test_url_modifyroom(self):
        url = reverse('roomModify')
        self.assertEqual(resolve(url).func, modifyRoom)