from  django.forms import ModelForm 
from .models import Post,Category
from  django import forms 
from parler.forms import TranslatableModelForm  
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission


class PostForm(TranslatableModelForm):
    # title_en = forms.CharField(label=_('title_en'))
    # title_ar = forms.CharField(label=_('title_ar'))
    # content_en = forms.CharField(label=_('content'))
    # content_ar = forms.CharField(label=_('content'))

    class Meta:
        model = Post
        #fields = ['title_en','title_ar','content_en','content_ar','category']
        fields = ['title','content','category']


    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(required=True,max_length=100,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'placeholder' : 'Title',
    }))
    # title_ar = forms.CharField(required=True,max_length=100,
    #     widget=forms.TextInput(attrs={
    #     "class": "form-control",
    #     "autocomplete": "off",
    #     'placeholder' : 'title_ar',
    # }))
    content = forms.CharField(required=True,
       widget=forms.Textarea(attrs={   
        "class": "form-control",
        'maxlength' : 10000000,
        'placeholder' : 'Content',
        "rows": 5,
        "style": "resize: none;"
    }))
    # content_ar = forms.CharField(required=True,
    #    widget=forms.Textarea(attrs={   
    #     "class": "form-control",
    #     'maxlength' : 10000000,
    #     'placeholder' : 'content_ar',
    #     "rows": 5,
    #     "style": "resize: none;"
    # }))
    use_required_attribute = None    

    def clean_title(self):
        title = self.cleaned_data.get('title')
            # Exclude the current instance's email from the check
        if self.instance and Post.objects.filter(translations__title=title).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("This Title is already in use by another Patient.")
        return title   
    
    # def clean_title_ar(self):
    #     title_ar = self.cleaned_data.get('title_ar')
    #         # Exclude the current instance's email from the check
    #     if self.instance and Post.objects.filter(translations__title=title_ar).exclude(pk=self.instance.id).exists():
    #         raise forms.ValidationError("This email address is already in use by another Patient.")
    #     return title_ar    


class GroupForm(ModelForm):
    name = forms.CharField(required=True,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Group Name',
    }))
    # permissions = forms.ModelChoiceField(
    #     queryset=Permission.objects.all(),
    #     #to_field_name='name',
    #     required=True,  
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    # permissions =forms.ChoiceField(
    #    required=True,
    #     widget=forms.Select(attrs={'class': 'my-custom-dropdown'})
    #       )
    use_required_attribute = None
  
    class Meta:
        model = Group
        #fields = '__all__'
        fields = ['id','name']

    # def clean_permissions(self):
    #     permissions = self.cleaned_data.get('username')
    #         # Exclude the current instance's username from the check
    #     if self.instance and Group.objects.filter(username=username).exclude(pk=self.instance.id).exists():
    #         raise forms.ValidationError("This Doctor name  is already in use by another user.")
    #     return permissions     

