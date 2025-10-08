from django.contrib.auth.models import AbstractUser
from django.db import models
from branches.models import Branch
from django.core.validators import MinLengthValidator,MaxLengthValidator 



class User(AbstractUser):
    ACTIVE = 'active'
    INACTIVE =  'inactive'
    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    email = models.EmailField(unique=True) 
    branche = models.ForeignKey(Branch, related_name='users', on_delete=models.CASCADE,null=True)
    phone = models.CharField(verbose_name='phone', max_length=30, validators=[MaxLengthValidator(limit_value=40, message="phone is too tooo!")]
    )
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default='INACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    username  = models.CharField(max_length=10,blank=False,unique=True,
						     validators=[MaxLengthValidator(limit_value=100, message="Text is too 8888888888888!")]
    )
    

   


 







            
                