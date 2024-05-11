# forms.py

from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']  # Replace 'image' with the actual field name in your model
