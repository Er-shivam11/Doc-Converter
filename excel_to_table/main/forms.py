from django import forms
from .models import ExcelData,UserPermission,UploadTemplate

class ExcelDataForm(forms.ModelForm):
    class Meta:
        model = ExcelData
        fields = ['excel_file']

class UserPermissionForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = "__all__"

class UploadWorkSheetForm(forms.ModelForm):
    class Meta:
        model = UploadTemplate
        fields = "__all__"
