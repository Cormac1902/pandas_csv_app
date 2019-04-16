from django import forms
from django.contrib.postgres import forms as pforms
from .models import ColumnCheck


class ColumnCheckForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'min_allowed' in kwargs:
            self.min_allowed = kwargs.pop('min_allowed')
        if 'max_allowed' in kwargs:
            self.max_allowed = kwargs.pop('max_allowed')
        if 'min_date_allowed' in kwargs:
            self.min_date_allowed = kwargs.pop('min_date_allowed')
        if 'max_date_allowed' in kwargs:
            self.max_date_allowed = kwargs.pop('max_date_allowed')

        super(ColumnCheckForm, self).__init__(*args, **kwargs)

        if hasattr(self, 'min_allowed'):
            self.fields['min_allowed'] = pforms.DecimalRangeField(min_value=self.min_allowed, max_value=self.max_allowed,
                                                                 required=False)
        '''if hasattr(self, 'max_allowed'):
            self.fields['max_allowed'] = forms.FloatField(min_value=self.min_allowed, max_value=self.max_allowed,
                                                          required=False)'''
        if hasattr(self, 'min_date_allowed'):
            self.fields['min_date_allowed'] = forms.DateTimeField(required=False)
        if hasattr(self, 'max_date_allowed'):
            self.fields['max_date_allowed'] = forms.DateTimeField(required=False)

    class Meta:
        model = ColumnCheck
        fields = ('null_values', 'special_characters')
