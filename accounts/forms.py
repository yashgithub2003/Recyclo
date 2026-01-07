from django import forms
from .models import ClientProfile

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['gender', 'date_of_birth', 'address', 'profile_photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
