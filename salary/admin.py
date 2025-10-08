from django.contrib import admin

from .models import *


class SalaryAdmin(admin.ModelAdmin):
        list_display = ('id', 'user')
admin.site.register(Salary, SalaryAdmin)


class salaryattributeAdmin(admin.ModelAdmin):
        list_display = ('id', 'user')
admin.site.register(salaryattribute, salaryattributeAdmin)


class BonusAttributesAdmin(admin.ModelAdmin):
        list_display = ('amount','created_at',)
admin.site.register(Bonus, BonusAttributesAdmin)





