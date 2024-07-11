from django import forms
from .models import Case

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['student_id','office', 'case_title', 'hearing_date', 'description','resolution']

