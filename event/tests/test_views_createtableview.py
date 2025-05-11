'''
Created on 2024/01/13

@author: t21cs029
'''
from django.test import TestCase, Client
from django.urls import reverse
from event.models import Table
from django.contrib.auth import get_user_model

class CreateTableViewTests(TestCase):
    def setUp(self):
        # テストに使用するユーザーを作成
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_get_context_data_without_login(self):
        # テスト用のURLを構築
        url = reverse('event:create_table')

        # テスト用のクライアントを作成
        client = Client()

        # ログインせずにテンプレートをリクエスト
        response = client.get(url)

        # コンテキストデータのテスト
        self.assertEqual(response.status_code, 200)  # ログインしていない場合でも成功

        self.assertIsNotNone(response.context)
        self.assertIn('form', response.context)
        self.assertIn('user_tables', response.context)
        self.assertIn('url_to_copy', response.context)
        self.assertIsNone(response.context['url_to_copy'])  # フォームがバインドされていないので None であるべき

        # ログインしていない場合のフォームがバインドされた状態のテスト
        form = response.context['form']
        form.is_bound = True
        form.is_valid()  # バインドされたフォームは妥当であると仮定

        # テンプレートをリクエスト
        response = client.get(url)

        self.assertEqual(response.status_code, 200)  # ログインしていない場合でも成功
        self.assertIsNotNone(response.context)
        self.assertIn('form', response.context)
        self.assertIn('user_tables', response.context)
        self.assertIn('url_to_copy', response.context)

        # フォームがバインドされ、妥当な場合、url_to_copy がセットされているかを再度テスト
        if form.is_bound and form.is_valid():
            self.assertIsNotNone(response.context['url_to_copy'])

    def test_get_context_data_with_login(self):
        # テスト用のURLを構築
        url = reverse('event:create_table')

        # テスト用のクライアントを作成
        client = Client()

        # ログインしてテンプレートをリクエスト
        client.login(username='testuser', password='testpassword')
        response = client.get(url)

        # コンテキストデータのテスト
        self.assertIsNotNone(response.context)
        self.assertIn('form', response.context)
        self.assertIn('user_tables', response.context)
        self.assertIn('url_to_copy', response.context)

        # フォームがバインドされている場合のテスト
        form = response.context['form']
        form.is_bound = True
        form.is_valid()  # バインドされたフォームは妥当であると仮定

        # テンプレートをリクエスト
        response = client.get(url)

        self.assertEqual(response.status_code, 200)  # ログインしていない場合でも成功
        self.assertIsNotNone(response.context)
        self.assertIn('form', response.context)
        self.assertIn('user_tables', response.context)
        self.assertIn('url_to_copy', response.context)
        # フォームがバインドされていないので None であるべき
        self.assertIsNone(response.context['url_to_copy'])

    def test_post_without_login(self):
        # テスト用のURLを構築
        url = reverse('event:create_table')

        # テスト用のクライアントを作成
        client = Client()

        # ログインしていない場合のPOSTリクエストを送信
        form_data = {
            'event': 'Test Event',
            'password': 'testpassword',
            'address': 'Test Address',
            'freetext': 'Test Free Text',
            'dates[]': ['2024-01-15'],
            'start_times[]': ['10:00'],
            'end_times[]': ['12:00'],
        }
        response = client.post(url, data=form_data, follow=True)

        # レスポンスのテスト
        self.assertEqual(response.status_code, 200)  # 成功時のステータスコードを指定
        self.assertRedirects(response, expected_url='/event/attendance/1/')  # リダイレクト先のURLを指定

        # データベースに保存されたテーブルと日時エントリを取得
        created_table = Table.objects.last()

        # テーブルが正しく作成されたかを検証
        self.assertIsNotNone(created_table)
        self.assertEqual(created_table.event, 'Test Event')
        self.assertEqual(created_table.password, 'testpassword')
        self.assertEqual(created_table.address, 'Test Address')
        self.assertEqual(created_table.freetext, 'Test Free Text')

        # 日時エントリが正しく作成されたかを検証
        date_time_entries = created_table.date_time_entries.all()

        # 日時エントリが正しく作成されたかを検証
        self.assertEqual(len(date_time_entries), 1)
        entry = date_time_entries[0]
        self.assertEqual(str(entry.date), '2024-01-15')
        self.assertEqual(str(entry.start_time.strftime('%H:%M')), '10:00')
        self.assertEqual(str(entry.end_time.strftime('%H:%M')), '12:00')

    def test_post_with_login(self):
        # テスト用のURLを構築
        url = reverse('event:create_table')

        # テスト用のクライアントを作成
        client = Client()

        # ログインしてPOSTリクエストを送信
        client.login(username='testuser', password='testpassword')
        form_data = {
            'event': 'Test Event',
            'password': 'testpassword',
            'address': 'Test Address',
            'freetext': 'Test Free Text',
            'dates[]': ['2024-01-15'],
            'start_times[]': ['10:00'],
            'end_times[]': ['12:00'],
        }
        response = client.post(url, data=form_data, follow=True)

        # レスポンスのテスト
        self.assertEqual(response.status_code, 200)  # 成功時のステータスコードを指定
        self.assertRedirects(response, expected_url='/event/attendance/1/')  # リダイレクト先のURLを指定

        # データベースに保存されたテーブルと日時エントリを取得
        created_table = Table.objects.last()

        # テーブルが正しく作成されたかを検証
        self.assertIsNotNone(created_table)
        self.assertEqual(created_table.event, 'Test Event')
        self.assertEqual(created_table.password, 'testpassword')
        self.assertEqual(created_table.address, 'Test Address')
        self.assertEqual(created_table.freetext, 'Test Free Text')

        # 日時エントリが正しく作成されたかを検証
        date_time_entries = created_table.date_time_entries.all()

        # 日時エントリが正しく作成されたかを検証
        self.assertEqual(len(date_time_entries), 1)
        entry = date_time_entries[0]
        self.assertEqual(str(entry.date), '2024-01-15')
        self.assertEqual(str(entry.start_time.strftime('%H:%M')), '10:00')
        self.assertEqual(str(entry.end_time.strftime('%H:%M')), '12:00')
