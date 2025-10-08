from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields  

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('name'),max_length=50),
    )
    def __str__(self):
        return self.name
    
    class Meta:
        #ordering = ('-created',)
        # db_table = ''
        # managed = True
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Post(TranslatableModel):
    category = models.ForeignKey(Category,related_name=_('category'),on_delete=models.SET_NULL,null=True)
    translations = TranslatedFields(
        title = models.CharField(_('title'),max_length=50,unique=True),
        meta={'unique_together': [('language_code', 'title')]},
        #meta={'unique_together': [('title'),]}, # Correct for unique_together
        content = models.TextField(_('content'))
    )

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created',)
        # db_table = ''
        # managed = True
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title
