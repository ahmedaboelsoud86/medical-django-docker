from django.db import models
from branches.models import Branch
from tools.models import Tool
# Create your models here.

class Pharmacy(models.Model):
    branch = models.ForeignKey(Branch, related_name='pharmacies', on_delete=models.CASCADE,null=True)
    tool = models.ForeignKey(Tool, related_name='pharmacies', on_delete=models.CASCADE,null=True)
    amount = models.IntegerField()

    class Meta:
        unique_together = ('branch', 'tool',) 

