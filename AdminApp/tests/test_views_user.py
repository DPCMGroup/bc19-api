from AdminApp.Views.user_view import loginUser, deleteUser, insertUser, modifyUser, userBookings
from AdminApp.Views import errorCode
from AdminApp.tests.test_base import TestViewBase


class TestViewsRoom(TestViewBase):

    def setUp(self):
        super().setUp()
        self.insertDefaultUser({"id": 1, "username": "mrossi", "password": "000", "name": "mario", "surname": "rossi",
                                "mail": "mario.rossi@gmail.com", "type": 0, "archived": 0})
        self.insertDefaultUser({"id": 2, "username": "mneri", "password": "000", "name": "mario", "surname": "neri",
                                "mail": "mario.neri@gmail.com", "type": 0, "archived": 0})

    def test_userBookings_GET(self):
        request = self.factory.get(self.user_bookings_url)
        res = userBookings(request, 1)
        self.assertEqual(res.status_code, 200)
        self.assertJSONEqual(res.content, [])

    def test_loginUser_POST(self):
        request = self.factory.post(self.user_login_url, {'username': 'mrossi', 'password': 'wrong'}, format='json')
        res = loginUser(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.user_login_url, {'username': 'mrossi', 'password': '000'}, format='json')
        res = loginUser(request)
        self.assertEqual(res.status_code, 200)
        self.assertJSONEqual(res.content,
                             {"id": 1, "username": "mrossi", "password": "000", "name": "mario", "surname": "rossi",
                              "mail": "mario.rossi@gmail.com", "type": 0, "archived": 0})

    def test_deleteUser_NoObj_GET(self):
        request = self.factory.get(self.user_delete_url)
        response = deleteUser(request, 400)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), errorCode.USER_THING + errorCode.NO_FOUND)

    def test_deleteUser_GET(self):
        request = self.factory.get(self.user_delete_url)
        response = deleteUser(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), errorCode.USER_THING + errorCode.OK)

    def test_getUsers_GET(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, 200)

    def test_modifyUser_POST(self):
        request = self.factory.post(self.room_modify_url,
                                    {"id": 1, "username": "mneri", "password": "000", "name": "mario",
                                     "surname": "rossi", "mail": "mario.rossi@gmail.com", "type": 0, "archived": 0},
                                    format='json')
        res = modifyUser(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.FAILURE)
        request = self.factory.post(self.room_modify_url,
                                    {"id": 100, "username": "mneri", "password": "000", "name": "mario",
                                     "surname": "rossi", "mail": "mario.rossi@gmail.com", "type": 0, "archived": 0},
                                    format='json')
        res = modifyUser(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.room_modify_url,
                                    {"id": 1, "username": "usernameMod", "password": "000", "name": "mario",
                                     "surname": "rossi", "mail": "mario.rossi@gmail.com", "type": 0, "archived": 0},
                                    format='json')
        res = modifyUser(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.OK)

    def test_inserUser_POST(self):
        requests = self.factory.post(self.user_insert_url,
                                     {"username": "mneri", "password": "000", "name": "mario", "surname": "neri",
                                      "mail": "mario.neri@gmail.com", "type": 0, "archived": 0}, format='json')
        res = insertUser(requests)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.FAILURE)
        requests = self.factory.post(self.user_insert_url,
                                     {"username": "nuovo", "password": "000", "name": "mario", "surname": "neri",
                                      "mail": "mario.neri@gmail.com", "type": 0, "archived": 0}, format='json')
        res = insertUser(requests)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.OK)
