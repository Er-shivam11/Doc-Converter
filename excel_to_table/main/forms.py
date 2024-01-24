from django import forms
from .models import ExcelData,UserPermission,UploadTemplate,UploadedForm,TempFormRelation

class ExcelDataForm(forms.ModelForm):
    class Meta:
        model = ExcelData
        fields = ['excel_file']

class UserPermissionForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = "__all__"

class RelationTempForm(forms.ModelForm):
    class Meta:
        model = TempFormRelation
        fields = "__all__"

class UploadWorkSheetForm(forms.ModelForm):
    class Meta:
        model = UploadTemplate
        fields = "__all__"


class FormSheet(forms.ModelForm):
    class Meta:
        model = UploadedForm
        fields = "__all__"