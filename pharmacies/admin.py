from django.contrib import admin

from .models import *


class PharmacyAdmin(admin.ModelAdmin):
        list_display = ('id',)


admin.site.register(Pharmacy, PharmacyAdmin)



