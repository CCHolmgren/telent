from django import forms
from .models import Image, ImageReport

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description', 'over_18', 'location']

class ImageReportForm(forms.ModelForm):
    class Meta:
        model = ImageReport
        fields = ['reason']