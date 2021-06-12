from django import forms
from .models import WasteCategoryPrice
from product.models import WasteCategory


class PriceForm(forms.ModelForm):
    class Meta:
        model = WasteCategoryPrice
        exclude = ["vendor",]

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }
    def __init__(self,*args,**kwargs):
        super (PriceForm,self ).__init__(*args,**kwargs)
        self.fields['category'].queryset = WasteCategory.objects.filter(status="pd")