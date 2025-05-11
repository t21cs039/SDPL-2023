'''
Created on 2023/12/12

@author: t21cs029
'''
from django import forms
from .models import Table, CustomUser, Attendee
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from event.models import DateAvailability
from django.forms.widgets import HiddenInput

# Create_Form:イベントテーブルのフォーム
class Create_Form(forms.ModelForm):
    # 追加のフィールド
    dates = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )  # イベント日程の日付を入力するためのフィールド
    start_times = forms.TimeField(input_formats=['%H:%M'], required=False)  # 開始時間を入力するためのフィールド
    end_times = forms.TimeField(input_formats=['%H:%M'], required=False)  # 終了時間を入力するためのフィールド

    freetext = forms.CharField(required=False, widget=forms.Textarea)  # フリーテキストを入力するためのフィールド

    class Meta:
        # フォームのメタ情報を設定
        model = Table  # フォームが対象とするモデル
        fields = ['event', 'password', 'address', 'freetext']  # フォームで扱うフィールド
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }  # フォームのウィジェットの設定

    def __init__(self, *args, **kwargs):
        super(Create_Form, self).__init__(*args, **kwargs)
        # 他の設定や初期化があればここに追加

    # 他に必要なメソッドやフィールドがあれば追加

    def get_absolute_url(self):
        # モデルが保存された後に遷移する URL を返す
        return reverse('event:attendance', kwargs={'pk': self.instance.pk})

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='メールアドレス')
    error_messages = {
        'invalid_login' : '正しいメールアドレスとパスワードを入力してください'
        }
    

class GuestLoginForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)
        if pk is not None:
            self.fields['pk'].initial = pk

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'comment']

    
class DateAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DateAvailability
        widgets = {'date' : HiddenInput}
        fields = ['date','availability']

    availability = forms.ChoiceField(
        choices=[
            ('yes', '◎'),
            ('maybe', '△'),
            ('no', '☓'),
        ],
        widget=forms.RadioSelect,
        required=True
    )

class Update_Form(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['event', 'password', 'address', 'freetext']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

    dates = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    start_times = forms.TimeField(input_formats=['%H:%M'], required=False)
    end_times = forms.TimeField(input_formats=['%H:%M'], required=False)
    
    freetext = forms.CharField(required=False, widget=forms.Textarea)
    
    def get_absolute_url(self):
        # モデルが保存された後に遷移する URL を返す
        return reverse('event:attendance', kwargs={'pk': self.instance.pk})
    

