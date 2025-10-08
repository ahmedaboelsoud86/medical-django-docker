from django.contrib import admin

from .models import *


class ToolAdmin(admin.ModelAdmin):
        list_display = ('id', 'name')


admin.site.register(Tool, ToolAdmin)



