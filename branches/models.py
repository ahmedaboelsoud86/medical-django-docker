from django.db import models 
from django.core.validators import MinLengthValidator,MaxLengthValidator 


class Branch(models.Model):
	name  = models.CharField(max_length=100,blank=False,unique=True,
							error_messages = {'max_length':'the field must less than  100 characters'},
							validators=[
							MinLengthValidator(3, 'the field must contain at least 3 characters')
							])
	
	class Meta:
		db_table = 'branches' 
		permissions = [
            ("can_deleteall_branches", "Can delete all branches"),
        ]

	def __str__(self):
		return self.name


