from django import forms

from .models import Document


# Document form for creating a new document
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document', 'type']
