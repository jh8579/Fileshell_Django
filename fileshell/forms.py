from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['dir_name', 'parent']

        def __init__(self, *args, **kwargs):
            super(FolderForm, self).__init__(*args, **kwargs)
            self.fields['folder'].required = False