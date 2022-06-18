from attr import attr
from django import forms


class ImageForm(forms.Form):
    image = forms.ImageField(
        label='',
        required=True,
        allow_empty_file=False,        
    )
