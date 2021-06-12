from django import forms
from .models import Waste, WasteCategory


class WasteCategoryForm(forms.ModelForm):
    class Meta:
        model = WasteCategory
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class WasteAddForm(forms.ModelForm):
    class Meta:
        model = Waste
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'image1': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'image3': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'waste_status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'location_lat': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'location_long': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self,*args,**kwargs):
        super (WasteAddForm,self ).__init__(*args,**kwargs)
        self.fields['category'].queryset = WasteCategory.objects.filter(status="pd")
