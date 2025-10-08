from django.db import models 
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .utils import image_resize
import sys
import os
#from django.db.models.signals import post_delete
#from django.dispatch import receiver

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/',null=True,blank=True)
    brief = models.TextField(blank=True,null=True,
        validators=[MaxLengthValidator(limit_value=1000, message="Text is too 8888888888888!")]
    )
    birthday = models.DateField(null=True,blank=True)

    class Meta:
        db_table = 'doctors' 
        permissions = [
            ("can_deleteall_doctors", "Can delete all doctors"),
        ]
         
		
 
    def __str__(self):
        return self.user.username
    

    def save(self, *args, **kwargs):
        image_resize(self.photo, 512, 512)
        super().save(*args, **kwargs)
    
    # def delete(self, *args, **kwargs):
    #     if self.photo:
    #         if os.path.isfile(self.photo.path):
    #             os.remove(self.photo.path)
    #     super().delete(*args, **kwargs)

    # def save (self, *args, **kwargs):
    
    #     pass
    
    # def save(self, *args, **kwargs):
    # # Opening the uploaded image
    #     img = Image.open(self.photo)
    #     if img.height > 200 or img.width > 200:
    #         output_size = (200, 200)
    #         img.thumbnail(output_size)
    #         img = img.convert('RGB')
    #         output = BytesIO()
    #         img.save(output, format='JPEG')
    #         output.seek(0)
    #         self.photo = InMemoryUploadedFile(output, 'ImageField',
    #                         f'{self.photo.name.split(".")[0]}.jpg',
    #                             'image/jpeg', sys.getsizeof(output),
    #                         None)
    #         super().save(*args, **kwargs)



   


