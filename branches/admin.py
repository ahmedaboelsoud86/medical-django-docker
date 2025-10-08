from django.contrib import admin

from .models import *


class BranchAdmin(admin.ModelAdmin):
        list_display = ('id', 'name')


admin.site.register(Branch, BranchAdmin)



