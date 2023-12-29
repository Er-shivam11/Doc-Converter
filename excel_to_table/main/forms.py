from django import forms
from .models import ExcelData,UserPermission

class ExcelDataForm(forms.ModelForm):
    class Meta:
        model = ExcelData
        fields = ['excel_file']

class TemplateForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = "__all__"
