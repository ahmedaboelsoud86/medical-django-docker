from django.contrib import admin

from .models import *


class PatientAdmin(admin.ModelAdmin):
        list_display = ('id','title','email','branch')
        list_display_links = ('id','title')
        list_editable = ['email','branch']
        search_fields = ['title']
        list_filter =  ['branch','gender']
        #fields = ['title']
        
admin.site.register(Patient, PatientAdmin)



class AppointmentAdmin(admin.ModelAdmin):
        list_display = ('id','doctor','patient','appdata')

admin.site.register(Appointment, AppointmentAdmin)


