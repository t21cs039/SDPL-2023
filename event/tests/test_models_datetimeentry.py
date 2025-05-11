'''
Created on 2024/01/13

@author: t21cs029
'''
from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from event.models import DateTimeEntry

class DateTimeEntryModelTests(TestCase):
    def test_create_datetime_entry(self):
        # 作成
        # 最初にデータベースに保存されている DateTimeEntry レコードの数を取得
        before_entries_count = DateTimeEntry.objects.all().count()

        date_test = datetime(2022, 1, 13)
        start_time_test = timezone.now().time()
        end_time_test = (timezone.now() + timezone.timedelta(hours=2)).time()

        entry = DateTimeEntry.objects.create(
            date=date_test,
            start_time=start_time_test,
            end_time=end_time_test
        )
        
        # 作成後のデータベースに保存されている DateTimeEntry レコードの数を再度取得
        after_entries_count = DateTimeEntry.objects.all().count()
        
        # 作成されたオブジェクトの各フィールドが期待通りの値か確認
        self.assertEqual(entry.date, date_test)
        self.assertEqual(entry.start_time, start_time_test)
        self.assertEqual(entry.end_time, end_time_test)
        
        #データベースに保存されているレコード数が1増えているか確認
        self.assertEqual(before_entries_count + 1, after_entries_count)

    def test_update_datetime_entry(self):
        # 修正
        # 最初にデータベースに保存されている DateTimeEntry レコードを作成
        entry = DateTimeEntry.objects.create(
            date=datetime(2022, 1, 13),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=2)).time()
        )
        
        # テスト実行前にデータベースに保存されている DateTimeEntry レコードの数を取得
        before_entries_count = DateTimeEntry.objects.all().count()
        
        # テスト用の日付、開始時刻、終了時刻を定義
        date_test = datetime(2022, 1, 14)
        start_time_test = timezone.now().time()
        end_time_test = (timezone.now() + timezone.timedelta(hours=3)).time()
        
        # 作成された DateTimeEntry オブジェクトのフィールドを修正
        entry.date = date_test
        entry.start_time = start_time_test
        entry.end_time = end_time_test
        
        # 修正を保存
        entry.save()
        
        # 修正後にデータベースに保存されている DateTimeEntry レコードの数を再度取得
        after_entries_count = DateTimeEntry.objects.all().count()
        
        #修正されたオブジェクトの各フィールドが期待通りの値か確認
        self.assertEqual(entry.date, date_test)
        self.assertEqual(entry.start_time, start_time_test)
        self.assertEqual(entry.end_time, end_time_test)
        
        # データベースに保存されているレコード数が変わっていないか確認
        self.assertEqual(before_entries_count, after_entries_count)

    def test_delete_datetime_entry(self):
        # 削除
        # 最初にデータベースに保存されている DateTimeEntry レコードを作成
        entry = DateTimeEntry.objects.create(
            date=datetime(2022, 1, 13),
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=2)).time()
        )
        
        # テスト実行前にデータベースに保存されている DateTimeEntry レコードの数を取得
        before_entries_count = DateTimeEntry.objects.all().count()
        
        # 作成された DateTimeEntry オブジェクトを削除
        entry.delete()
        
        # 削除後にデータベースに保存されている DateTimeEntry レコードの数を再度取得
        after_entries_count = DateTimeEntry.objects.all().count()
        
        # データベースに保存されているレコード数が減っているか確認
        self.assertEqual(before_entries_count - 1, after_entries_count)
        
        