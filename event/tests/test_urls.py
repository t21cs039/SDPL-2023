'''
Created on 2024/01/13

@author: t21cs029
'''
from django.test import TestCase
from django.urls import resolve
from event.views import CreateTableView, LoginView, RegisterView, LogoutView, AttendanceView

app_name = 'event'

class EventUrlsTests(TestCase):
    def test_create_table_url(self):
        # create_table ビューの URL パスを解決し、正しいビュークラスに関連付けられていることを確認
        view = resolve('/event/create_table/')
        self.assertEqual(view.func.view_class, CreateTableView)

    def test_login_url(self):
        # login ビューの URL パスを解決し、正しいビュークラスに関連付けられていることを確認
        view = resolve('/event/login/')
        self.assertEqual(view.func.view_class, LoginView)

    def test_register_url(self):
        # register ビューの URL パスを解決し、正しいビュークラスに関連付けられていることを確認
        view = resolve('/event/register/')
        self.assertEqual(view.func.view_class, RegisterView)

    def test_logout_url(self):
        # logout ビューの URL パスを解決し、正しいビュークラスに関連付けられていることを確認
        view = resolve('/event/logout/')
        self.assertEqual(view.func.view_class, LogoutView)
        
    def test_attendance_url(self):
        # attendance ビューの URL パスを解決し、正しいビュークラスに関連付けられていることを確認
        view = resolve('/event/attendance/1/')
        self.assertEqual(view.func.view_class, AttendanceView)
