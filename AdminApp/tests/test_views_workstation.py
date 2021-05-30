from AdminApp.Views.workstation_view import insertWorkstation, deleteWorkstation, modifyWorkstation, \
    getWorkstationStatus, sanizieWorkstation
from AdminApp.Views import errorCode
from AdminApp.tests.test_base import TestViewBase
from datetime import datetime


class TestViewsWorkstation(TestViewBase):

    def setUp(self):
        super().setUp()
        self.insertDefaultRoom({'id': 1, 'roomname': 'testRoomName', 'xroom': 10, 'yroom': 10, 'archived': 0, 'unavailable': 0})
        self.insertDefaultWorkstation(
            {'id': 1, 'tag': 'aa aa aa aa aa', 'workstationname': 'testName1', 'xworkstation': 0, 'yworkstation': 0,
             'idroom': 1, 'state': 0, 'sanitized': 0, 'archived': 0})
        self.insertDefaultWorkstation(
            {'id': 2, 'tag': '22 aa aa aa aa', 'workstationname': 'testName2', 'xworkstation': 0, 'yworkstation': 1,
             'idroom': 1, 'state': 0, 'sanitized': 0, 'archived': 0})
        self.insertDefaultUser({"id": 1, "username": "mrossi", "password": "000", "name": "mario", "surname": "rossi",
                                "mail": "mario.rossi@gmail.com", "type": 0, "archived": 0})

    def test_sanitizeWorkstation_POST(self):
        request = self.factory.post(self.workstation_sanitize_url, {'tag': 'sbagliato', 'idUser': 1}, format='json')
        res = sanizieWorkstation(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.WORK_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.workstation_sanitize_url, {'tag': 'aa aa aa aa aa', 'idUser': 400},
                                    format='json')
        res = sanizieWorkstation(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.USER_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.workstation_sanitize_url, {'tag': 'aa aa aa aa aa', 'idUser': 1,
                                                                    'data': datetime.now()},
                                    format='json')
        res = sanizieWorkstation(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.SANITIZE_THING + errorCode.OK)

    def test_getInfoWorkstation_POST(self):
        request = self.factory.post(self.workstation_getinfo_url, {'tag': 'sbagliato'}, format='json')
        res = getWorkstationStatus(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.WORK_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.workstation_getinfo_url, {'tag': 'aa aa aa aa aa'}, format='json')
        res = getWorkstationStatus(request)
        self.assertEqual(res.status_code, 200)
        self.assertJSONEqual(res.content,
                             {'roomName': 'testRoomName', 'bookedToday': 0, 'workId': 1, 'workName': 'testName1',
                              'workSanitized': 0, 'workStatus': 0})

    def test_modifyWorkstation_POST(self):
        request = self.factory.post(self.workstation_modify_url,
                                    {'id': 400, 'tag': 'a2 aa aa aa aa', 'workstationname': 'modifyName',
                                     'xworkstation': 2, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                     'sanitized': 0, 'archived': 0}, format='json')
        res = modifyWorkstation(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.WORK_THING + errorCode.NO_FOUND)
        request = self.factory.post(self.workstation_modify_url,
                                    {'id': 1, 'tag': '22 aa aa aa aa', 'workstationname': 'modifyName',
                                     'xworkstation': 0, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                     'sanitized': 0, 'archived': 0}, format='json')
        res = modifyWorkstation(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.WORK_THING + errorCode.FAILURE)
        request = self.factory.post(self.workstation_modify_url,
                                    {'id': 1, 'tag': 'a2 aa aa aa aa', 'workstationname': 'modifyName',
                                     'xworkstation': 0, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                     'sanitized': 0, 'archived': 0}, format='json')
        res = modifyWorkstation(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(res.content), errorCode.WORK_THING + errorCode.OK)

    def test_insertWorkstation_POST(self):
        requestSucess = self.factory.post(self.workstation_insert_url,
                                          {'tag': 'aa aa aa aa bb', 'workstationname': 'testname',
                                           'xworkstation': 1, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                           'sanitized': 0, 'archived': 0}, format='json')
        requestFail = self.factory.post(self.workstation_insert_url,
                                        {'tag': 'aa aa aa aa bb', 'workstationname': 'testname',
                                         'xworkstation': 1, 'yworkstation': 0, 'idroom': 1, 'state': 0,
                                         'sanitized': 0, 'archived': 0}, format='json')
        responseS = insertWorkstation(requestSucess)  # insert first time, no big deal
        self.assertEqual(responseS.status_code, 200)
        self.assertEqual(int(responseS.content), errorCode.WORK_THING + errorCode.OK)
        responseF = insertWorkstation(requestFail)  # insert second time, its an error cause there is already one
        self.assertEqual(responseF.status_code, 200)
        self.assertEqual(int(responseF.content), errorCode.WORK_THING + errorCode.FAILURE)

    def test_getWorkstations_GET(self):
        response = self.client.get(self.workstation_list_url)
        self.assertEqual(response.status_code, 200)

    def test_deleteWorkstation_NoObj_GET(self):
        request = self.factory.get(self.workstation_delete_url)
        response = deleteWorkstation(request, 400)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), errorCode.WORK_THING + errorCode.NO_FOUND)

    def test_deleteWorkstation_GET(self):
        request = self.factory.get(self.workstation_delete_url)
        response = deleteWorkstation(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.content), errorCode.WORK_THING + errorCode.OK)
