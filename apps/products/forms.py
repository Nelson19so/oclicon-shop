from django import forms
from .models import ProductSpecification

# product specification form
class ReadOnlyProductSpecificationForm(forms.ModelForm):

    class Meta:
        model = ProductSpecification
        fields = ['memory', 'size', 'storage']
        widget = {
            'memory': forms.TextInput(attrs={'id': 'memory'}),
            'size': forms.TextInput(attrs={'id': 'size'}),
            'storage': forms.TextInput(attrs={'id': 'storage'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True  # makes input text not editable
