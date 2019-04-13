from django import forms
from .models import ColumnCheck


class ColumnCheckForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'min_allowed' in kwargs:
            self.min_allowed = kwargs.pop('min_allowed')
            self.max_allowed = kwargs.pop('max_allowed')

        super(ColumnCheckForm, self).__init__(*args, **kwargs)

        if hasattr(self, 'min_allowed'):
            self.fields['min_allowed'] = forms.FloatField(min_value=self.min_allowed, max_value=self.max_allowed)
            self.fields['max_allowed'] = forms.FloatField(min_value=self.min_allowed, max_value=self.max_allowed)

    class Meta:
        model = ColumnCheck
        fields = ('null_values', 'special_characters')
