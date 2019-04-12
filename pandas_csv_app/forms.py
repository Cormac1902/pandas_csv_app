from django import forms
from .models import ColumnCheck


class ColumnCheckForm(forms.ModelForm):
    class Meta:
        model = ColumnCheck
        fields = ('null_values', 'special_characters')
