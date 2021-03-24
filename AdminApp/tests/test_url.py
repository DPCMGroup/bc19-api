from django.test import SimpleTestCase
from django.urls import reverse, resolve
from AdminApp.views import insertWorkstation, deleteWorkstation, getWorkstations


class TestUrls(SimpleTestCase):

    def test_url_getworkstation(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func, getWorkstations)

    def test_url_insertworkstation(self):
        url = reverse('insert')
        self.assertEqual(resolve(url).func, insertWorkstation)

    def test_url_deleteworkstation(self):
        url = reverse('delete', args=[1])
        self.assertEqual(resolve(url).func, deleteWorkstation)