from django.db import models 
from django.core.validators import MinLengthValidator,MaxLengthValidator 


class Tool(models.Model):
	name  = models.CharField(max_length=100,blank=False,unique=True,
						    error_messages = {'max_length':'the field must less than  100 characters'},
						    validators=[
							MinLengthValidator(3, 'the field must contain at least 3 characters')
							])
	price = models.DecimalField(max_digits=10, decimal_places=2)  
	def __str__(self):
		return self.name	
