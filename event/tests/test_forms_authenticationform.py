'''
Created on 2024/01/19

@author: t21cs039
'''
from django.test import TestCase, Client
from event.forms import RegisterForm, LoginForm
from event.models import CustomUser

class AuthenticateFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='test', email='newuser@example.com',password='trypassword')

    def test_register_form_valid(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = RegisterForm(data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'wrongpassword',  # This should make the form invalid
        }
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_login_form_valid(self):
        
        data = {
            'username':'newuser@example.com',
            'password':'trypassword',
        }
        
        form = LoginForm(data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        data = {
            'username': 'testuser@example.com',
            'password': 'wrongpassword',  # This should make the form invalid
        }
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

    
    