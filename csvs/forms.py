from django import forms
from .models import TeacherCsv

class TeacherCsvModelForm(forms.ModelForm):
    class Meta:
        model = TeacherCsv
        fields = ('filez',)