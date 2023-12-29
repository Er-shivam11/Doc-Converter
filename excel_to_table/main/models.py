from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models

class ExcelData(models.Model):
    excel_file = models.FileField(upload_to='uploads/')


class Usertable(models.Model):        
    type_name = models.CharField(verbose_name="Type Name", max_length=150, unique=True,null=True, blank=True)
    password=models.CharField(max_length=200)
    status=models.BooleanField()
    class Meta:
        db_table = 'tbl_usertable'
    def __str__(self) -> str:
        return self.type_name

class TemplateMaster(models.Model):
    name=models.CharField(max_length=200,verbose_name='template name',  blank=False, null=True)
    status=models.BooleanField()
    class Meta:
        db_table = 'tbl_templatemaster'
    def __str__(self) -> str:
        return self.name

class UserPermission(models.Model):
    user_table=models.ForeignKey(Usertable,verbose_name='User name', on_delete=models.SET_NULL, null=True)
    template_master=models.ForeignKey(TemplateMaster,verbose_name='template name', on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'tbl_userpermission'
    def __str__(self) -> str:
        return self.template_master

class TemplateDetail(models.Model):
    step=models.IntegerField()
    description=models.CharField(max_length=200)
    std_value=models.CharField(max_length=200)
    obs_value=models.CharField(max_length=200)
    start_time=models.CharField(max_length=200)
    end_time=models.CharField(max_length=200)
    class Meta:
        db_table = 'tbl_templatedetail'
    
    
    