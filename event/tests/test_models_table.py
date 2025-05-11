'''
Created on 2024/01/13

@author: t21cs029
'''
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from event.models import Table, DateTimeEntry
from datetime import datetime
from django.utils import timezone

class TableModelTests(TestCase):

    def setUp(self):
        # テストで使用する初期データのセットアップ
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.datetime_entry = DateTimeEntry.objects.create(
            date=datetime(2022, 1, 13),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=2)).time()
        )
        
    def test_create_table(self):
        # 作成
        before_tables_count = Table.objects.all().count()

        table = Table.objects.create(
            event='Test Event',
            password='Test123',
            address='Test Address',
            freetext='Test Free Text',
            user=self.user
        )

        after_tables_count = Table.objects.all().count()

        self.assertEqual(table.event, 'Test Event')
        self.assertEqual(table.password, 'Test123')
        self.assertEqual(table.address, 'Test Address')
        self.assertEqual(table.freetext, 'Test Free Text')
        self.assertEqual(table.user, self.user)
        self.assertEqual(before_tables_count + 1, after_tables_count)
        
    def test_update_table(self):
        # 修正
        table = Table.objects.create(
            event='Test Event',
            password='Test123',
            address='Test Address',
            freetext='Test Free Text',
        )

        before_tables_count = Table.objects.all().count()

        new_event = 'Updated Event'
        new_password = 'Updated123'
        new_address = 'Updated Address'
        new_freetext = 'Updated Free Text'

        table.event = new_event
        table.password = new_password
        table.address = new_address
        table.freetext = new_freetext
        table.save()

        after_tables_count = Table.objects.all().count()

        self.assertEqual(table.event, new_event)
        self.assertEqual(table.password, new_password)
        self.assertEqual(table.address, new_address)
        self.assertEqual(table.freetext, new_freetext)
        self.assertEqual(before_tables_count, after_tables_count)
    
    def test_delete_table(self):
        # 削除
        table = Table.objects.create(
            event='Test Event',
            password='Test123',
            address='Test Address',
            freetext='Test Free Text',
            user=self.user
        )

        before_tables_count = Table.objects.all().count()

        table.delete()

        after_tables_count = Table.objects.all().count()

        self.assertEqual(before_tables_count - 1, after_tables_count)

    def test_get_absolute_url(self):
        # get_absolute_url メソッドのテスト
        table = Table.objects.create(
            event='Test Event',
            password='Test123',
            address='Test Address',
            freetext='Test Free Text',
            user=self.user
        )

        expected_url = reverse('event:attendance', args=[str(table.pk)])
        self.assertEqual(table.get_absolute_url(), expected_url)
    
    
    
    
    