from django.db import models
from django.conf import settings
from django.db.models import Max
from django.contrib.auth import get_user_model
from django.utils.text import Truncator



class Room(models.Model):
	#name = models.CharField(max_length=255)
	# other fields...

	def __str__(self):
		return self.id

# class Inbox(models.Model):
# 	title  = models.CharField(max_length=100,blank=True,null=True)
# 	body = models.TextField(blank=True,null=True)
# 	seen = models.BooleanField()
# 	room = models.IntegerField()
# 	sender =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="inbox_sender")
# 	recipient  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="inbox_recipient")
# 	timestamp = models.DateTimeField(auto_now_add=True)	


# class Message(models.Model):
# 	room = models.ForeignKey(Room, on_delete=models.CASCADE)
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# 	content = models.TextField()
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return f'{self.user.username}: {self.content}'
	
class testmessage(models.Model):
	title = models.CharField(max_length=100, blank=False,null=False)
	room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name="testmessages")
	sender =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="testmessage_sender")
	recipient  = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="testmessage_recipient")
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	
	# def __str__(self):
	# 	return self.title    
 
	def __str__(self):
		truncted_content = Truncator(self.content)
		return truncted_content.chars(100)

	# def __str__(self):
	# 	return f'{self.sender.username} : {self.content} <br>'    