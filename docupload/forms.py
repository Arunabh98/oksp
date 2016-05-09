from django import forms

from .models import Documentation


class DocUploadForm(forms.Form):
    '''Form for documentation file upload'''

    name = forms.CharField(max_length=100)
    doc_file = forms.FileField()

    class Meta(object):
        model = Documentation
        fields = [
            "name", 
            "doc_file", 
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Title','class': 'form-control'}),
        }
