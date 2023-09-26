from django import forms
from .models import HellpDesk

class HelpForm(forms.ModelForm):
     class Meta:
        model = HellpDesk
        fields = ['name', 'phone', 'email', 'description', 'priority']