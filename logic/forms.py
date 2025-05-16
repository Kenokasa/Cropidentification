from django import forms
from .models import PlantScan

class PlantScanForm(forms.ModelForm):
    class Meta:
        model = PlantScan
        fields = ['image', 'scan_type']
        widgets = {
            'scan_type': forms.RadioSelect(choices=PlantScan.SCAN_TYPES)
        }