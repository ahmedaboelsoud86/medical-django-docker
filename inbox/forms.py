from  django.forms import ModelForm # type: ignore
from .models import testmessage
from  django import forms # type: ignore
from  users.models import User 

class messageForm(ModelForm):

    
 
    class Meta:
        model = testmessage
        fields = ['recipient','title','content']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop the 'user' from kwargs
        super().__init__(*args, **kwargs)
        # You can now use self.user within the form, for example, to filter a queryset
        if self.user:
            self.fields['recipient'].queryset=User.objects.exclude(pk=self.user.pk)

    
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        #to_field_name='name',
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title = forms.CharField(required=True,
        widget=forms.TextInput(attrs={
        "class": "form-control",
        "autocomplete": "off",
        'maxlength' : 10000000,
        'placeholder' : 'Title',
        }))
    content = forms.CharField(required=True,
       widget=forms.Textarea(attrs={   
        "class": "form-control",
        'maxlength' : 10000000,
        'placeholder' : 'Message',
        "rows": 5,
        "style": "resize: none;"
    }))
    use_required_attribute = None    
