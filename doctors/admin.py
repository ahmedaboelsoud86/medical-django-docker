from django.contrib import admin

from .models import *
from users.models import User

class DoctorAdmin(admin.ModelAdmin):
        list_display = ('id', 'user')


admin.site.register(Doctor, DoctorAdmin)



class DoctorInline(admin.StackedInline):
        model = Doctor

class UserAdmin(admin.ModelAdmin):
        model = User
        field = []
        inlines = [DoctorInline]

# class DoctorAdmin(admin.ModelAdmin):
#         list_display = ('id', 'user')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)




