from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


admin.site.unregister(Group)



class PatientAdmin(admin.ModelAdmin):
        list_display = ('id','title','email','branch')
        list_display_links = ('id','title')
        list_editable = ['email','branch']
        search_fields = ['title']
        list_filter =  ['branch','gender']
        #fields = ['title']
        
admin.site.register(Patient, PatientAdmin)



class AppointmentAdmin(admin.ModelAdmin):
        list_display = ('id','doctor','patient','appdata','combine_x_y')
        
        def combine_x_y(self,obj):
                return "{} - {}".format(obj.doctor,obj.patient)

admin.site.register(Appointment, AppointmentAdmin)

class ExpenseAdmin(admin.ModelAdmin):
        list_display = ('amount','patient','tool','tool_calculated')
        
        def tool_calculated(self,obj):
                return obj.amount * obj.tool.price

admin.site.register(Expense, ExpenseAdmin)

