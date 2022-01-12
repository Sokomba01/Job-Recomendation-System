from django import forms
from Job_Recommendation.models import *
from django.contrib.auth.models import User
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(label='',widget=forms.FileInput(attrs={'style' : 'display:none;','value':'choosefile',
                                                                  'placeholder':'choosefile'}))