from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.views.generic import View, TemplateView
from .forms import (
    Create_Form, 
    LoginForm, 
    RegisterForm, 
    GuestLoginForm, 
    AttendeeForm, 
    Update_Form,
    DateAvailabilityForm
)
from .models import Table, Attendee, DateAvailability, DateTimeEntry
from utils.weather_util import get_weather_data
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.db import transaction
from pickle import FALSE

# CreateTableView:イベントテーブルを作成するビュー
class CreateTableView(TemplateView):
    # テンプレート名を指定
    template_name = 'event/create_table.html'
    
    def get_context_data(self, **kwargs):
        # コンテキストデータを取得するメソッド
        context = super().get_context_data(**kwargs)
        
        # Create_Form インスタンスを生成
        form = Create_Form()

        # フォームが送信され、有効な場合
        if form.is_bound and form.is_valid():
            # インスタンスを一時的に保存し、URLを生成
            table_instance = form.save(commit=False)
            context['url_to_copy'] = self.request.build_absolute_uri(table_instance.get_absolute_url())

            # 住所を元に天気データを取得
            weather_data = get_weather_data(table_instance.address)
            context['weather_data'] = weather_data
        else:
            context['url_to_copy'] = None

        # フォームをコンテキストに追加
        context['form'] = form
        
        # ログインしている場合、ユーザーに関連するテーブルを取得
        if self.request.user.is_authenticated:
            user_tables = Table.objects.filter(user=self.request.user)
            context['user_tables'] = user_tables
        else:
            context['user_tables'] = []
            
        return context

    def post(self, request, *args, **kwargs):
        # POST メソッドの処理
        form = Create_Form(request.POST)
        
        # フォームが有効な場合
        if form.is_valid():
            # フォームからデータを取得
            event = form.cleaned_data['event']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            freetext = form.cleaned_data['freetext']
            
            # ログインしている場合はユーザーを、していない場合は AnonymousUser を取得
            if request.user.is_authenticated:
                user = request.user if request.user.is_authenticated else AnonymousUser()
            else :
                user = None

            # イベントテーブルのインスタンスを作成
            table_instance = Table.objects.create(
                event=event,
                password=password,
                address=address,
                freetext=freetext,
                user=user
            )

            # 日程ごとのデータを取得し、テーブルに関連付けて保存
            dates = request.POST.getlist('dates[]')
            start_times = request.POST.getlist('start_times[]')
            end_times = request.POST.getlist('end_times[]')

            for date, start_time, end_time in zip(dates, start_times, end_times):
                table_instance.date_time_entries.create(
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )

            # 参加者画面へリダイレクト
            return redirect(reverse_lazy('event:attendance', kwargs={'pk': table_instance.pk}))

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'event/login.html'
    
    def post(self, request, *args, **kwargs):
        next_url = self.request.POST.get('next', None)
        
        if not next_url:
            next_url = self.request.GET.get('next', reverse('event:create_table'))        
        
        response = super().post(request, *args, **kwargs)
        
        redirect_url = reverse('event:login') + f"?next={next_url}"
        
        #ログインできたら、前の画面・ホーム画面に戻る
        if self.request.user.is_authenticated:
            return redirect(next_url)
        else:
            return redirect(redirect_url)
        
        return response
    
class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'event/register.html'
    
    #登録できたら、前の画面・ホーム画面に戻る
    def form_invalid(self, form):
        messages.error(self.request, '会員登録に失敗しました。正しい情報を入力してください。')
        next_url = self.request.POST.get('next', None)
        
        if not next_url:
            next_url = self.request.GET.get('next', reverse('event:create_table'))        
        return redirect(next_url)
    
    def get_success_url(self):
        messages.success(self.request, '会員登録完了!ログインしてください')
        next_url = self.request.POST.get('next', None)
        
        if not next_url:
            next_url = self.request.GET.get('next', reverse('event:create_table'))        
        return next_url
    
class LogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('event:create_table')
    
class AttendanceView(View):
    template_name = 'event/attendance.html'

    def get(self, request, pk) :
        table_instance = get_object_or_404(Table, pk=pk)

        # 日程、開始時間、終了時間でソート
        date_time_entries = table_instance.date_time_entries.all().order_by('date', 'start_time', 'end_time')
        
        
        attendees = table_instance.attendees.all()
        user_tables = []
        
        if self.request.user.is_authenticated:
            user_tables = Table.objects.filter(user=self.request.user)
            if table_instance not in user_tables:
                table_instance.user = self.request.user
                table_instance.save()
                user_tables = Table.objects.filter(user=self.request.user)

                

        # Get weather data based on the address
        weather_data = get_weather_data(table_instance.address)
        
        # Create DateAvailabilityFormSet
        DateAvailabilityFormSet = modelformset_factory(
            DateAvailability,
            form=DateAvailabilityForm,
            extra=len(date_time_entries),  # Set 'extra' to the number of date_time_entries
        )
        
        # Get existing DateAvailability instances for this table
        date_availabilities = DateAvailability.objects.none()

        # Create the formset instance with initial data
        formset = DateAvailabilityFormSet(
            queryset=date_availabilities,
            initial=[{'date': entry} for entry in date_time_entries],  # Initial data for each form
        )

        attendee_availability = DateAvailability.objects.filter(attendee__table = table_instance)
        best_date = date_time_entries.first()
        if len(attendees) == 0 :
            best_date = None
        best = 0
        for date in date_time_entries:
            index = 0
            for availabilities in attendee_availability:
                
                if availabilities.date == date :
                    if availabilities.availability == 'yes':
                        index += 2
                    elif availabilities.availability == 'maybe':
                        index +=1
                    else:
                        index +=0
        
            if index > best :
                best = index
                best_date = date            
        context = {
            'table_instance': table_instance,
            'url_to_copy': self.request.build_absolute_uri(table_instance.get_guest_url()),
            'date_time_entries': date_time_entries,  # フォーマットを変更したリストを使用
            'attendees': attendees,
            'attendee_form': AttendeeForm(),
            'date_availability_formset': formset,
            'weather_data': weather_data,
            'attendee_availability': attendee_availability,
            'user_tables': user_tables,
            'best_date': best_date,
        }

        return render(request, self.template_name, context)
    
    
    def post(self, request, pk):
        table_instance = get_object_or_404(Table, pk=pk)
        date_time_entries = table_instance.date_time_entries.all().order_by('date', 'start_time', 'end_time')
        attendees = Attendee.objects.filter(table=table_instance)
        
        attendee_form = AttendeeForm(request.POST)
        DateAvailabilityFormSet = modelformset_factory(
                DateAvailability,
                form=DateAvailabilityForm,
                extra=len(date_time_entries),
            )
        
        if attendee_form.is_valid():
            date_availabilities = DateAvailability.objects.none()
            formset = DateAvailabilityFormSet(request.POST, queryset=date_availabilities)
     
            if formset.is_valid():
                # Save the formset
                attendee = attendee_form.save(commit=False)
                attendee.table = table_instance
                attendee.save()
        
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.attendee = attendee
                    instance.save()  
            
             
            return redirect(reverse('event:attendance', kwargs={'pk': table_instance.pk}))

        context = {
            'table_instance': table_instance,
            'date_time_entries': date_time_entries,
            'attendees': attendees,
            'attendee_form': attendee_form,
        }

        return render(request, self.template_name, context)
    
class EditAttendanceView(View):
    template_name = 'event/edit_attendance.html'

    def get(self, request, pk, attendee_id):
        table_instance = get_object_or_404(Table, pk=pk)
        attendee = get_object_or_404(Attendee, id=attendee_id, table=table_instance)

        # 日程、開始時間、終了時間でソート
        date_time_entries = table_instance.date_time_entries.all().order_by('date', 'start_time', 'end_time')

        attendees = table_instance.attendees.all()
        user_tables = []
        
        if self.request.user.is_authenticated:
            user_tables = Table.objects.filter(user=self.request.user)
            if table_instance not in user_tables:
                table_instance.user = self.request.user
                table_instance.save()
                user_tables = Table.objects.filter(user=self.request.user)

                

        # Get weather data based on the address
        weather_data = get_weather_data(table_instance.address)
        # Get existing DateAvailability instances for this table
        date_availabilities = DateAvailability.objects.filter(attendee=attendee)

        # Create DateAvailabilityFormSet
        DateAvailabilityFormSet = modelformset_factory(
            DateAvailability,
            form=DateAvailabilityForm,
            extra=len(date_availabilities),  # Set 'extra' to the number of date_time_entries
        )
        
        # Create the formset instance with initial data
        formset = DateAvailabilityFormSet(
            queryset=DateAvailability.objects.none(),
            initial=[{'date': date, 'availability': entry.availability} for entry, date in zip(date_availabilities, date_time_entries)]
            
        )

        attendee_availability = DateAvailability.objects.filter(attendee__table = table_instance)
        
        attendee_form = AttendeeForm(instance=attendee)
        
        best_date = date_time_entries.first()

        best = 0
        for date in date_time_entries:
            index = 0
            for availabilities in attendee_availability:
                
                if availabilities.date == date :
                    if availabilities.availability == 'yes':
                        index += 2
                    elif availabilities.availability == 'maybe':
                        index +=1
                    else:
                        index +=0
        
            if index > best :
                best = index
                best_date = date
                
        context = {
            'table_instance': table_instance,
            'url_to_copy' : self.request.build_absolute_uri(table_instance.get_absolute_url()),
            'date_time_entries': date_time_entries,
            'attendees': attendees,
            'attendee_form': attendee_form,
            'date_availability_formset': formset,
            'weather_data': weather_data,
            'attendee_availability' : attendee_availability,
            'user_tables' : user_tables,
            'attendee_id' : attendee_id,
            'attendee_instance' : attendee,
            'best_date' : best_date,

        }

        return render(request, self.template_name, context)
    
    
    def post(self, request, pk, attendee_id):
        table_instance = get_object_or_404(Table, pk=pk)
        date_time_entries = table_instance.date_time_entries.all().order_by('date', 'start_time', 'end_time')
        attendees = Attendee.objects.filter(table=table_instance)
        attendee = get_object_or_404(Attendee, id=attendee_id, table=table_instance)

        attendee_form = AttendeeForm(request.POST, instance=attendee)
        
        date_availabilities = DateAvailability.objects.filter(attendee=attendee)

        DateAvailabilityFormSet = modelformset_factory(
                DateAvailability,
                form=DateAvailabilityForm,
                extra=len(date_availabilities),
            )
        

        if attendee_form.is_valid():
        
            formset = DateAvailabilityFormSet(request.POST, queryset=date_availabilities)

            if formset.is_valid():
                attendee_form.save()
                date_availabilities.delete()
                
                # Save the formset
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.attendee = attendee
                    instance.save()
            
            return redirect(reverse('event:attendance', kwargs={'pk': table_instance.pk}))

        context = {
            'table_instance': table_instance,
            'date_time_entries': date_time_entries,
            'attendees': attendees,
            'attendee_form': attendee_form,
            'date_availability_formset': formset,
        }

        return render(request, self.template_name, context)
    
    
class GuestLoginView(View):
    template_name = 'event/guestlogin.html'
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # Get the Table instance with the given pk
        get_object_or_404(Table, pk=pk)
        form = GuestLoginForm(pk=pk)
        return render(request, 'event/guestlogin.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            pk = self.kwargs['pk']
            password = form.cleaned_data.get('password')
            # Try to get the Table instance with the given pk
            try:
                table_instance = Table.objects.get(pk=pk, password=password)
                return redirect('event:attendance', pk=pk)
            except Table.DoesNotExist:
                pass
    
        return render(request, self.template_name, {'form':form, 'error':'パスワードが間違っています。'})

class UpdateTableView(TemplateView):
    template_name = 'event/update_table.html'
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        table_instance = get_object_or_404(Table, pk=pk)
        form = Update_Form(instance=table_instance)
        user_tables = []
        
        if self.request.user.is_authenticated:
            user_tables = Table.objects.filter(user=self.request.user)
            if table_instance not in user_tables:
                table_instance.user = self.request.user
                table_instance.save()
                user_tables = Table.objects.filter(user=self.request.user)
        return render(request, self.template_name, {'form': form, 'table': table_instance,'user_tables':user_tables})
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        table_instance = get_object_or_404(Table, pk=pk)
        attendees = Attendee.objects.filter(table=table_instance)
        attendee_availability = DateAvailability.objects.filter(attendee__table = table_instance)

        form = Update_Form(request.POST, instance=table_instance)
        if form.is_valid():
            event = form.cleaned_data['event']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            freetext = form.cleaned_data['freetext']

            table_instance.event = event
            table_instance.password = password
            table_instance.address = address
            table_instance.freetext = freetext

            # Remove old date_time_entries
            old_n = len(table_instance.date_time_entries.all())
            table_instance.date_time_entries.clear()

            dates = request.POST.getlist('dates[]')
            start_times = request.POST.getlist('start_times[]')
            end_times = request.POST.getlist('end_times[]')

            for date, start_time, end_time in zip(dates, start_times, end_times):
                date_time_entry = DateTimeEntry.objects.create(
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )
                
                table_instance.date_time_entries.add(date_time_entry)
            
            table_instance.save()
            
            #参加者のデートエントリーを更新する
            with transaction.atomic():
                for attendee in attendees:
                    n = 0
                    
                    date_availabilities = DateAvailability.objects.filter(attendee=attendee)
                    
                    # Add the new date_time_entries to each attendee's availability
                    for date_time_entry, date_availability in zip(table_instance.date_time_entries.all(), date_availabilities):
                        
                        attendee_availability = date_availability.availability

                        date_availability.delete()
                        DateAvailability.objects.create(
                            attendee=attendee,
                            date=date_time_entry,
                            availability=attendee_availability
                                )   

                        
                    #新しいエントリーを全部Xに初期化する
                    for date_time_entry in table_instance.date_time_entries.all():
                        if n >= old_n:
                            attendee_availability = 'no'
                            DateAvailability.objects.create(
                                attendee=attendee,
                                date=date_time_entry,
                                availability=attendee_availability
                                    ) 
                        else :
                            n += 1
                       
                    #削除
                    date_availabilities = DateAvailability.objects.filter(attendee=attendee)
                    for date_availability in date_availabilities:
                        delete=True
                        for date_time_entry in table_instance.date_time_entries.all():

                            if date_availability.date == date_time_entry :
                                delete = False
                        
                        if delete == True:
                            date_availability.delete()
                                
            table_instance.save()
            
            return redirect(reverse_lazy('event:attendance', kwargs={'pk': pk}))
        return render(request, self.template_name, {'form': form, 'table': table_instance})
    