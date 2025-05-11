'''
Created on 2024/01/15

@author: t21cs062
'''
from django.test import TestCase, Client
from django.urls import reverse
from event.models import Table

class GuestLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.table = Table.objects.create(
            event='Test Event',
            password='Test Password',
            address='Test Address',
            freetext='Test Freetext'
        )

    def test_guest_login_view(self):
        response = self.client.get(reverse('event:guestlogin', kwargs={'pk': self.table.pk}))
        self.assertEqual(response.status_code, 200)

    def test_guest_login_post(self):
        response = self.client.post(reverse('event:guestlogin', kwargs={'pk': self.table.pk}), {'pk': self.table.pk, 'password': 'Test Password'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
