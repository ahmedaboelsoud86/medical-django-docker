from django.db import models 



class Branch(models.Model):
	name  = models.CharField(max_length=100,blank=False,unique=True,
							error_messages = {
           							'max_length':'the name  Branch Must less than  100 characters',
                  					'unique':"unique fil555ed"},
							)
	
	class Meta:
		db_table = 'branches' 
		permissions = [
            ("can_deleteall_branches", "Can delete all branches"),
        ]

	def __str__(self):
		return self.name


