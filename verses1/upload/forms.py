from django import forms
from .models import UploadFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['file']