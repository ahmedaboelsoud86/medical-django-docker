from django.contrib import admin

from .models import *


class PatientAdmin(admin.ModelAdmin):
        list_display = ('id','title','email')


admin.site.register(Patient, PatientAdmin)



class AppointmentAdmin(admin.ModelAdmin):
        list_display = ('id','doctor','patient','appdata')

admin.site.register(Appointment, AppointmentAdmin)


