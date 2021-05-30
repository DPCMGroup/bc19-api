from AdminApp.Views.room_view import insertRoom, deleteRoom, modifyRoom
from AdminApp.Views import errorCode
from AdminApp.tests.test_base import TestViewBase


class TestViewsRoom(TestViewBase):

    def setUp(self):
        super().setUp()
        self.insertDefaultRoom({'id': 1, 'roomname': 'defaultRoom1', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0})
        self.insertDefaultRoom({'id': 2, 'roomname': 'defaultRoom2', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0})

    def test_deleteWorkstation_NoObj_GET(self):
        request = self.factory.get(self.workstation_delete_url)
        response = deleteRoom(request, 400)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), errorCode.ROOM_THING + errorCode.NO_FOUND)

    def test_deleteWorkstation_GET(self):
        request = self.factory.get(self.workstation_delete_url)
        response = deleteRoom(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), errorCode.ROOM_THING + errorCode.OK)

    def test_getRooms_GET(self):
        response = self.client.get(self.room_list_url)
        self.assertEqual(response.status_code, 200)

    def test_insertRoom_POST(self):
        requestS = self.factory.post(self.room_insert_url,
                                     {'roomname': 'testRoomName', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0},
                                     format='json')
        requestF = self.factory.post(self.room_insert_url,
                                     {'roomname': 'testRoomName', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0},
                                     format='json')
        res = insertRoom(requestS)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.ROOM_THING + errorCode.OK)
        res = insertRoom(requestF)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.ROOM_THING + errorCode.FAILURE)

    def test_modifyRoom_POST(self):
        request = self.factory.post(self.room_modify_url,
                                    {'id': 1, 'roomname': 'defaultRoom2', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0},
                                    format='json')
        res = modifyRoom(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.ROOM_THING + errorCode.FAILURE)
        request = self.factory.post(self.room_modify_url,
                                    {'id': 100, 'roomname': 'defaultRoom2', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0},
                                    format='json')
        res = modifyRoom(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.ROOM_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.room_modify_url,
                                    {'id': 1, 'roomname': 'modifyName', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0},
                                    format='json')
        res = modifyRoom(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.ROOM_THING + errorCode.OK)
