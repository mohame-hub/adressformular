from django import forms
from .models import Adresse

class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ['strasse', 'hausnummer', 'plz', 'ort', 'bundesland']
