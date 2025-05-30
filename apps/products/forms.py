from django import forms
from .models import ProductSpecification

class ReadOnlyProductSpecificationForm(forms.ModelForm):
    
    class Meta:
        model = ProductSpecification
        fields = ['memory', 'size', 'storage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True  # makes input text not editable
            field.widget.attrs['disabled'] = True  # prevents form submission
