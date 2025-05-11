'''
Created on 2024/01/13

@author: t21cs029
'''
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from event.models import Table, DateTimeEntry, Weather
from datetime import datetime

class WeatherModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.datetime_entry = DateTimeEntry.objects.create(
            date=datetime(2022, 1, 13),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=2)).time()
        )
        self.table = Table.objects.create(
            event='Test Event',
            password='Test123',
            address='Test Address',
            freetext='Test Free Text',
            user=self.user
        )

    def test_create_weather_entry(self):
        # 作成
        before_weather_entries_count = Weather.objects.all().count()

        weather_entry = Weather.objects.create(
            table=self.table,
            date=datetime(2022, 1, 14),
            data={'temperature': 25, 'conditions': 'Sunny'}
        )

        after_weather_entries_count = Weather.objects.all().count()

        self.assertEqual(weather_entry.table, self.table)
        self.assertEqual(weather_entry.date, datetime(2022, 1, 14))
        self.assertEqual(weather_entry.data, {'temperature': 25, 'conditions': 'Sunny'})
        self.assertEqual(before_weather_entries_count + 1, after_weather_entries_count)
        
