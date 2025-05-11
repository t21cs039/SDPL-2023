from django.db import models
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from utils.weather_util import get_weather_data
from event.models import Table, Attendee, DateTimeEntry, CustomUser, Weather

class AttendanceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testusername' ,email='testuser@example.com', password='testpassword')  # Use CustomUser
        self.table = Table.objects.create(
            user=self.user,
            event='Test Event',
            password='testpassword',
            address='Test Address',
            freetext='Test Free Text'
        )
        self.attendee = Attendee.objects.create(table=self.table, name='Test Attendee')
        self.date_entry = DateTimeEntry.objects.create(
            date='2024-01-01',
            start_time='12:00',
            end_time='14:00'
        )
        
        # Create a sample Weather entry for testing
        self.weather_entry = Weather.objects.create(
            table_id=1,  # Replace with a valid table ID
            date='2024-01-01',
            data={
                "temperature": 25,
                "humidity": 60,
                "weather": "Sunny",
                "wind_speed": 10,
            }
        )

    def test_event_details_displayed(self):
        # イベントの詳細が正しく表示されることを確認
        response = self.client.get(reverse('event:attendance', kwargs={'pk': self.table.pk}))
        self.assertContains(response, 'Test Event')
        # 他の詳細情報も同様に確認

    def test_copy_url(self):
        # 1. Clientオブジェクトを作成してビューを呼び出す
        response = self.client.get(reverse('event:attendance', kwargs={'pk': self.table.pk}))
        # 2. レスポンスの中から想定しているURLが含まれているかを確認する
        expected_url = reverse('event:guestlogin', kwargs={'pk': self.table.pk})
        self.assertIn(expected_url, response.content.decode())


    def test_weather_model_str(self):
        self.assertEqual(str(self.weather_entry), f"Weather for {date.today()} - {self.weather_entry.data}")

    def test_weather_view(self):
        response = self.client.get(reverse('your_url_name'))  # Replace with the actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>5日間の天気情報</h2>')
        self.assertQuerysetEqual(response.context['weather_data'], [repr(self.weather_entry.data)], transform=str)


    def test_attendee_registration(self):
        # 参加者の新規登録が正しく機能することを確認
        data = {'name': 'New Attendee', 'availability': 'yes', 'comment': 'Test Comment'}
        response = self.client.post(reverse('event:attendance', kwargs={'pk': self.table.pk}), data)
        self.assertEqual(response.status_code, 302)  # 成功のリダイレクト
        new_attendee = Attendee.objects.get(name='New Attendee')
        self.assertIsNotNone(new_attendee)

    def test_attendee_editing(self):
        # 参加者の情報編集が正しく機能することを確認
        attendee = Attendee.objects.create(table=self.table, name='Test Attendee')
        data = {'name': 'Updated Attendee', 'availability': 'maybe', 'comment': 'Updated Comment'}
        response = self.client.post(reverse('event:edit_attendance', kwargs={'pk': self.table.pk, 'attendee_id': attendee.pk}), data)
        self.assertEqual(response.status_code, 302)  # 成功のリダイレクト
        updated_attendee = Attendee.objects.get(pk=attendee.pk)
        self.assertEqual(updated_attendee.name, 'Updated Attendee')
        # 他の編集内容も同様に確認

    def test_event_edit_page_navigation(self):
        # イベント編集ページへのアクセスが正しく機能することを確認
        response = self.client.get(reverse('event:edit_attendance', kwargs={'pk': self.table.pk, 'attendee_id': 1}))
        self.assertEqual(response.status_code, 200)  # 正常なレスポンス