'''
Created on 2024/01/14

@author: t21cs062
'''
from django.urls import reverse
from django.contrib.auth import get_user_model
from event.models import Table, DateTimeEntry
from django.test import TestCase, Client


# Create your tests here.
class UpdateTableViewTest(TestCase):
    def setUp(self):
        # テスト用のユーザーとテーブルを作成します
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(event='Test Event', password='Test Password', address='Test Address', freetext='Test Freetext', user=self.user)
        self.entry = DateTimeEntry.objects.create(date='2022-01-01', start_time='10:00:00', end_time='12:00:00')
        self.table.date_time_entries.add(self.entry)

        # テストクライアントを作成します
        self.client = Client()
    
    def test_post_request_data(self):
        # ユーザーを認証します
        self.client.login(username='testuser', password='testpass')
    
        # 更新するデータを作成します
        updated_data = {
            'event': 'Updated Event',
            'password': 'Updated Password',
            'address': 'Updated Address',
            'freetext': 'Updated Freetext',
            'dates[]': ['2022-01-02'],
            'start_times[]': ['11:00:00'],
            'end_times[]': ['13:00:00'],
        }
    
        # POSTリクエストを送信します
        response = self.client.post(reverse('event:update_table', args=[self.table.pk]), data=updated_data)
    
        # レスポンスがリダイレクト（ステータスコード 302）であることを確認します
        self.assertEqual(response.status_code, 302)
    
        # リクエストのPOSTデータが正しいことを確認します
        self.assertEqual(response.wsgi_request.POST['event'], 'Updated Event')
        self.assertEqual(response.wsgi_request.POST['password'], 'Updated Password')
        self.assertEqual(response.wsgi_request.POST['address'], 'Updated Address')
        self.assertEqual(response.wsgi_request.POST['freetext'], 'Updated Freetext')
        self.assertEqual(response.wsgi_request.POST.getlist('dates[]'), ['2022-01-02'])
        self.assertEqual(response.wsgi_request.POST.getlist('start_times[]'), ['11:00:00'])
        self.assertEqual(response.wsgi_request.POST.getlist('end_times[]'), ['13:00:00'])

    def test_update_table_view(self):
        # ユーザーを認証します
        self.client.login(username='testuser', password='testpass')

        # 更新するデータを作成します
        updated_data = {
            'event': 'Updated Event',
            'password': 'Updated Password',
            'address': 'Updated Address',
            'freetext': 'Updated Freetext',
            'dates[]': ['2022-01-02'],
            'start_times[]': ['11:00:00'],
            'end_times[]': ['13:00:00'],
        }

        # POSTリクエストを送信します
        response = self.client.post(reverse('event:update_table', args=[self.table.pk]), data=updated_data)

        # レスポンスがリダイレクト（ステータスコード 302）であることを確認します
        self.assertEqual(response.status_code, 302)

        # テーブルが更新されたことを確認します
        self.table.refresh_from_db()
        self.assertEqual(self.table.event, 'Updated Event')
        self.assertEqual(self.table.password, 'Updated Password')
        self.assertEqual(self.table.address, 'Updated Address')
        self.assertEqual(self.table.freetext, 'Updated Freetext')
"""
        # 日程エントリが更新されたことを確認します
        entry = self.table.date_time_entries.first()
        self.assertEqual(entry.date.strftime('%Y-%m-%d'), '2022-01-02')
        self.assertEqual(entry.start_time.strftime('%H:%M:%S'), '11:00:00')
        self.assertEqual(entry.end_time.strftime('%H:%M:%S'), '13:00:00')"""
