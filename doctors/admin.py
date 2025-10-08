from django.contrib import admin

from .models import *


class DoctorAdmin(admin.ModelAdmin):
        list_display = ('id', 'user')


admin.site.register(Doctor, DoctorAdmin)




