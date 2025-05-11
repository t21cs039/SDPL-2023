'''
Created on 2024/01/13

@author: t21cs029
'''
from django.test import TestCase
from django.urls import reverse
from event.forms import Create_Form
from event.models import Table

class CreateFormTests(TestCase):
    def test_valid_form(self):
        # 有効なデータを使用してフォームをテスト
        data = {
            'event': 'Test Event',
            'password': 'Test123',
            'address': 'Test Address',
            'freetext': 'Test Free Text',
            'dates': '2022-01-13',
            'start_times': '12:00',
            'end_times': '14:00',
        }
        form = Create_Form(data)
        self.assertTrue(form.is_valid())
        # 任意入力を空欄にしたフォームをテスト
        data = {
            'event': 'Test Event',
            'password': 'Test123',
            'address': 'Test Address',
            'freetext': '',
            'dates': '2022-01-13',
            'start_times': '12:00',
            'end_times': '14:00',
        }
        form = Create_Form(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # 有効でないデータを使用してフォームをテスト
        data = {
            'event': '',  # 必須フィールドが空
            'password': 'Test123',
            'address': 'Test Address',
            'freetext': 'Test Free Text',
            'dates': '2022-01-13',
            'start_times': '12:00',
            'end_times': '14:00',
        }
        form = Create_Form(data)
        self.assertFalse(form.is_valid())
        
        '''
        # パスワードが空白でも有効なフォームをテスト
        data = {
            'event': 'Test Event',
            'password': '',
            'address': 'Test Address',
            'freetext': 'Test Free Text',
            'dates': '2022-01-13',
            'start_times': '12:00',
            'end_times': '14:00',
        }
        form = Create_Form(data)
        self.assertTrue(form.is_valid())
        '''

    def test_get_absolute_url(self):
        # get_absolute_url メソッドが正しく動作するかをテスト
        table_instance = Table.objects.create(
            event='Test Event',
            password='Test123',
            address='Test Address',
            freetext='Test Free Text'
        )
        form = Create_Form(instance=table_instance)
        expected_url = reverse('event:attendance', kwargs={'pk': table_instance.pk})
        self.assertEqual(form.get_absolute_url(), expected_url)
        
        # 別のインスタンスで get_absolute_url メソッドが正しく動作するかをテスト
        table_instance = Table.objects.create(
            event='Another Event',
            password='Another123',
            address='Another Address',
            freetext='Another Free Text'
        )
        form = Create_Form(instance=table_instance)
        expected_url = reverse('event:attendance', kwargs={'pk': table_instance.pk})
        self.assertEqual(form.get_absolute_url(), expected_url)
        
        