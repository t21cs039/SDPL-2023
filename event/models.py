from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# ref: https://rahmanfadhil.com/django-login-with-email/
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
class DateTimeEntry(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    def formatted_date(self):
        return self.date.strftime('%Y-%m-%d')  # このフォーマットは YYYY-MM-DD です
    def formatted_start_time(self):
        return self.start_time.strftime('%H:%M')  # このフォーマットは HH:MM です
    def formatted_end_time(self):
        return self.end_time.strftime('%H:%M')  # このフォーマットは HH:MM です
    
class Table(models.Model):
    event = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    freetext = models.TextField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tables', null=True, blank=True)
    date_time_entries = models.ManyToManyField(DateTimeEntry, related_name='table_entries')
    def get_absolute_url(self):
        return reverse('event:attendance', args=[str(self.pk)])
    def get_guest_url(self):
        return reverse('event:guestlogin', args=[str(self.pk)])
    
class Weather(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='weather_entries')
    date = models.DateField()
    data = models.JSONField()

    def __str__(self):
        return f"Weather for {self.date} - {self.data}"
    
class DateAvailability(models.Model):
    attendee = models.ForeignKey('Attendee', on_delete=models.CASCADE, related_name='date_availabilities')
    date = models.ForeignKey(DateTimeEntry, on_delete=models.CASCADE, blank=False)
    availability = models.CharField(
        max_length=10,
        choices=[
            ('yes', '◎'),
            ('maybe', '△'),
            ('no', '☓'),
        ],
        default='yes',
    )

class Attendee(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='attendees')
    name = models.CharField(max_length=255)
    
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_availability_for_date(self, date):
        try:
            date_availability = self.date_availabilities.get(date=date)
            return date_availability.availability
        except DateAvailability.DoesNotExist:
            return None
