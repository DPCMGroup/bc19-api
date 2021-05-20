from django.test import SimpleTestCase
from django.urls import reverse, resolve
from AdminApp.Views.user_view import insertUser, modifyUser, getUsers, deleteUser, loginUser, userBookings


class TestUrlsUser(SimpleTestCase):

    def test_url_getroom(self):
        url = reverse('userList')
        self.assertEqual(resolve(url).func, getUsers)

    def test_url_insertroom(self):
        url = reverse('userInsert')
        self.assertEqual(resolve(url).func, insertUser)

    def test_url_deleteroom(self):
        url = reverse('userDelete', args=[1])
        self.assertEqual(resolve(url).func, deleteUser)

    def test_url_modifyroom(self):
        url = reverse('userModify')
        self.assertEqual(resolve(url).func, modifyUser)

    def test_url_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, loginUser)

    def test_url_userBookings(self):
        url = reverse('userBookings', args=[1])
        self.assertEqual(resolve(url).func, userBookings)