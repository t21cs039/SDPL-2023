'''
Created on 2023/12/08

@author: t21cs039
'''
from django.urls import path
from . import views
from .views import AttendanceView

app_name = 'event'

urlpatterns = [
    path('create_table/', views.CreateTableView.as_view(), name='create_table'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('guestlogin/<int:pk>/', views.GuestLoginView.as_view(), name='guestlogin'),
    path('attendance/<int:pk>/', views.AttendanceView.as_view(), name='attendance'),
    path('attendance/<int:table_id>/', views.AttendanceView.as_view(), name='attendance'),
    path('update_table/<int:pk>/', views.UpdateTableView.as_view(), name='update_table'),
    path('attendance/<int:pk>/<int:attendee_id>', views.EditAttendanceView.as_view(), name='edit_attendance'),


]
