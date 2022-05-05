from .models import *
from django.forms import ModelForm
from django import forms

# hasta formu
class PatientForm(ModelForm):

    class Meta:
        model=Patient
        fields=["first_name","last_name","mail"]

# recete formu
class ReceteForm(ModelForm):
    
    class Meta:
        model=Recete
        fields=['hasta','tags',]
            
        widgets = {
            
            'tags': forms.CheckboxSelectMultiple()
            }

# ilac formu
class MedicineForm(ModelForm):
    class Meta:
        model=Medicine
        fields=["ilac_adi","prospekt","ilacfiyati"]
