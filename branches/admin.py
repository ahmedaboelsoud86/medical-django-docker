from django.contrib import admin

from .models import *


class BranchAdmin(admin.ModelAdmin):
        list_display = ('id', 'name')


admin.site.register(Branch, BranchAdmin)

# ٍSome-Customise-Admin
admin.site.site_header = "medical-projct"
admin.site.site_title = "medical-projct"

