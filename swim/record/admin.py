from django.contrib import admin

from record.models import Person, Menue, Training, Result_Time, Users

# Register your models here.
# admin.site.register()

admin.site.register(Person)
admin.site.register(Menue)
admin.site.register(Training)
# admin.site.register(Distance)
admin.site.register(Result_Time)
admin.site.register(Users)
