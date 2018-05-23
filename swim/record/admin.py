from django.contrib import admin

from record.models import Person, Menue, Time_Result, Users

# Register your models here.

admin.site.register(Person)
admin.site.register(Menue)
admin.site.register(Time_Result)
admin.site.register(Users)
