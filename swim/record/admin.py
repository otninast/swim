from django.contrib import admin

from record.models import Menue, Result_Time, User_Info, DayMenu, TrainingMenu


admin.site.register(Menue)
admin.site.register(DayMenu)
admin.site.register(TrainingMenu)
admin.site.register(Result_Time)
# admin.site.register(Rap_Time)
admin.site.register(User_Info)
