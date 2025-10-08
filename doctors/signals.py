from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Doctor
import os   
@receiver(post_delete, sender=Doctor)
def delete_parent_on_child_delete(sender, instance, **kwargs):
    # Check if the parent still exists before attempting to delete
    # This is important to prevent errors if the parent was already deleted
    # due to cascading deletions from other children or direct deletion.
    if instance.user:
        instance.user.delete()

@receiver(post_delete, sender=Doctor)
def delete_image_file(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
