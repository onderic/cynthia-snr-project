from django import forms
from .models import Case,Image

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['student_id','office', 'case_title', 'hearing_date', 'description','resolution']



class GeeksForm(forms.Form):
    name = forms.CharField(max_length=200)
    images = forms.FileField(required=False)
