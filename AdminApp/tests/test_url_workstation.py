from django.test import SimpleTestCase
from django.urls import reverse, resolve
from AdminApp.Views.workstation_view import insertWorkstation, deleteWorkstation, getWorkstations, modifyWorkstation, getWorkstationStatus, sanizieWorkstation


class TestUrlsWorkstation(SimpleTestCase):

    def test_url_getworkstation(self):
        url = reverse('workstationList')
        self.assertEqual(resolve(url).func, getWorkstations)

    def test_url_insertworkstation(self):
        url = reverse('workstationInsert')
        self.assertEqual(resolve(url).func, insertWorkstation)

    def test_url_deleteworkstation(self):
        url = reverse('workstationDelete', args=[1])
        self.assertEqual(resolve(url).func, deleteWorkstation)

    def test_url_modifyworkstation(self):
        url = reverse('workstationModify')
        self.assertEqual(resolve(url).func, modifyWorkstation)

    def test_url_workstationgetinfo(self):
        url = reverse('workstationInfo')
        self.assertEqual(resolve(url).func, getWorkstationStatus)

    def test_url_sanitizeworkstation(self):
        url = reverse('workstationSanitize')
        self.assertEqual(resolve(url).func, sanizieWorkstation)

