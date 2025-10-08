from  django.forms import ModelForm 
from .models import Post,Category
from  django import forms 
from parler.forms import TranslatableModelForm  
from django.utils.translation import gettext_lazy as _


class PostForm(TranslatableModelForm):
    title_en = forms.CharField(label=_('title_en'))
    title_ar = forms.CharField(label=_('title_ar'))
    content_en = forms.CharField(label=_('content'))
    content_ar = forms.CharField(label=_('content'))

    class Meta:
        model = Post
        fields = ['title_en','title_ar','content_en','content_ar','category']


    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title_en = forms.CharField(required=True,max_length=50,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'placeholder' : 'title_en',
    }))
    title_ar = forms.CharField(required=True,max_length=50,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'placeholder' : 'title_ar',
    }))
    content_en = forms.CharField(required=True,
       widget=forms.Textarea(attrs={   
        "class": "form-control",
        'maxlength' : 10000000,
        'placeholder' : 'content_en',
        "rows": 5,
        "style": "resize: none;"
    }))
    content_ar = forms.CharField(required=True,
       widget=forms.Textarea(attrs={   
        "class": "form-control",
        'maxlength' : 10000000,
        'placeholder' : 'content_ar',
        "rows": 5,
        "style": "resize: none;"
    }))
    use_required_attribute = None    

    def clean_title_en(self):
        title_en = self.cleaned_data.get('title_en')
        if self.instance and Post.objects.filter(translations__title=title_en).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This Title en is already in use by another Post.")
        return title_en

    def clean_title_ar(self):
        title_ar = self.cleaned_data.get('title_ar')
        if self.instance and Post.objects.filter(translations__title=title_ar).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This Title ar is already in use by another Post.")
        return title_ar      
        

