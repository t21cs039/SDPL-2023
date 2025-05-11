from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser

class AuthenticationTest(TestCase):
    def setUp(self):
            self.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com',password='testpassword')

    #ログインの確認
    def test_login_view(self):
        login_url = reverse('event:login') 
        next_url = reverse('event:create_table')#ログイン後デフォルトURL
        
        #ログインする
        response = self.client.post(login_url, {'username': 'testuser@example.com', 'password': 'testpassword'})
        
        #ログインしているかの確認
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # レスポンスのテスト
        self.assertEqual(response.status_code, 302)  # 成功時のステータスコードを指定
        self.assertEqual(response.url, next_url) #デフォルトURLに戻る
     
    #他の画面からログインする場合
    def test_login_view_with_next_parameter(self):
        next_url = reverse('event:register')  #前の画面
        login_url = reverse('event:login') + f"?next={next_url}"
        
        response = self.client.post(login_url, {'username': 'testuser@example.com', 'password': 'testpassword', 'next': next_url})
        
        #ログイン後、前の画面に戻る
        self.assertRedirects(response, next_url)
    
    #会員登録
    def test_registration_view(self):
        register_url = reverse('event:register')
        login_url = reverse('event:login')

        response = self.client.post(register_url, {'email': 'newuser@example.com', 'username': 'newuser', 'password1': 'syazwani', 'password2': 'syazwani'})
        
        # レスポンスのテスト
        self.assertEqual(response.status_code, 302)  # 成功時のステータスコードを指定
        self.assertEqual(response.url, reverse('event:create_table')) #会員登録後デフォルトURL
        
        #できたメッセージを確認する
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '会員登録完了!ログインしてください')

        #登録した情報でログインする
        response = self.client.post(login_url, {'username': 'newuser@example.com', 'password': 'syazwani'})
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    #他の画面から会員登録する場合   
    def test_registration_view_with_next_parameter(self):
        next_url = reverse('event:login')#前の画面
        register_url = reverse('event:register') + f"?next={next_url}"
        
        response = self.client.post(register_url, {'email': 'newuser@example.com', 'username': 'newuser', 'password1': 'syazwani', 'password2': 'syazwani'})
        
        #登録できた後、前の画面に移動する
        self.assertRedirects(response, next_url)
    
    #ログアウト    
    def test_logout_view(self):
        #ログインする
        login_url = reverse('event:login')
        self.client.post(login_url, {'username': 'testuser', 'password': 'testpassword'})

        logout_url = reverse('event:logout')
        response = self.client.get(logout_url)
        
        #デフォルトURLに戻る
        self.assertRedirects(response, reverse('event:create_table'))

        #ユーザタイプを変わる
        self.assertTrue(isinstance(response.wsgi_request.user, AnonymousUser))
