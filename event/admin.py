from django.contrib import admin
from .models import Table, CustomUser
from event.models import Attendee, DateAvailability, DateTimeEntry, Weather

# Register your models here.
admin.site.register(Table)
admin.site.register(CustomUser)
admin.site.register(Attendee)
admin.site.register(DateAvailability)
admin.site.register(DateTimeEntry)
admin.site.register(Weather)