from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render
from .forms import ExcelDataForm
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import UserPermissionForm,UploadWorkSheetForm,FormSheet,RelationTempForm
import os
import pandas as pd
from .models import TemplateDetail,UploadTemplate,FormDetail,UploadedForm,TempFormRelation
import numpy as np
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from pathlib import Path





def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('home')  # Superuser, redirect to the 'home' page
                else:
                    return redirect('home')  
                
            else:
                if username == '' or password == '':
                    messages.error(
                        request, message='Please Enter Username and Passowrd Correctly')
                else:
                    messages.error(
                        request, message='Username or Password not correct')

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def addtemplate(request):
    form = UploadWorkSheetForm()

    if request.method == 'POST':
        form = UploadWorkSheetForm(request.POST, request.FILES)
        if form.is_valid():
            
            upload_template_instance = form.save()
            
            # Read the Excel file using pandas
            try:
                tid=upload_template_instance.id
                worksheet_name = upload_template_instance.worksheet_name
                file_path=upload_template_instance.worksheet_file
                creator_name = upload_template_instance.creator.type_name
                print(creator_name)
                data = pd.read_excel(upload_template_instance.worksheet_file.path)
                data = data.iloc[:, :-2]
                data = data.loc[:, ~data.columns.str.startswith('Unnamed')]
                data1 = data.drop(0).replace(0, pd.NA).fillna("")
                data=data1.dropna(how='all')
        
        
                data = data.rename(columns={
                    'Step': 'description',
                    'Actual Readings': 'actual_readings',
                    'Start Time': 'start_time',
                    'End Time (hour)': 'end_time'
                })
                print(data)
                data['Step No.'] = data['Step No.'].str.strip()
                print(type(data))
                print(data.head(10))
                csv_file_path = os.path.join(settings.MEDIA_ROOT, 'formatted_data.csv')
                data.to_csv(csv_file_path, index=False)

                for index, row in data.iterrows():
                # Extract values from the DataFrame
                    step = row[0]
                    description = row[1]
                    std_value = row[2]  # Placeholder for std_value, you need to extract it based on your data
                    obs_value = 'N/A'  # Assuming the observed value is in the 8th column
                    start_time = 'N/A'   # Placeholder for start_time, you need to extract it based on your data
                    end_time = 'N/A'     # Placeholder for end_time, you need to extract it based on your data
                    step = ''.join(char for char in step if char.isdigit())
                    if not step:
                        continue
                # Create an instance of the TemplateDetail model and save it to the database
                    TemplateDetail.objects.create(
                        step=step,
                        description=description,
                        std_value=std_value,
                        obs_value=obs_value,
                        start_time=start_time,
                        end_time=end_time,
                        creator=creator_name,
                        upload_template_id=tid

                    )
                    # FormDetail.objects.create(
                    #     step=step,
                    #     description=description,
                    #     std_value=std_value,
                    #     obs_value=obs_value,
                    #     start_time=start_time,
                    #     end_time=end_time,
                    #     creator=creator_name,


                    # )
                
                # Print the values

            except pd.errors.EmptyDataError:
                print(form.errors)
            
            return redirect('selecttemplate')
        else:
            # Handle form errors - you can print them or log them for debugging
            print(form.errors)

    name=UploadTemplate.objects.all()
    print('name',name)

    context = {
        'form': form
    }
    return render(request, 'addtemplate.html', context)



def home(request):
    return render(request,"home.html")

def selecttemplate(request):
    tform=UserPermissionForm
    if request.method == 'POST':
        count_form = UserPermissionForm(request.POST, request.FILES)
        if count_form.is_valid():

            count_form.save()
            return redirect('formuploaded')
        else:
            print(count_form.errors)
    else:
        count_form = UserPermissionForm()
    context = {
        'tform': tform}
    return render(request, 'selecttemp.html', context)




def formuploaded(request):
    tform=FormSheet
    if request.method == 'POST':
        count_form = FormSheet(request.POST, request.FILES)
        if count_form.is_valid():   
            count_form.save()
            return redirect('editform')
        else:
            print(count_form.errors)
    else:
        count_form = FormSheet()
    context = {
        'tform': tform} 
    return render(request, 'addform.html', context)



def edit(request):
    tempform=TemplateDetail.objects.all()
    fid = UploadedForm.objects.latest('id')
    tid = UploadTemplate.objects.latest('id')
    tempid=tid.id
    formid=fid.id

    for formdetails in tempform:
        FormDetail.objects.create(
        step=formdetails.step,
        description=formdetails.description,
        std_value=formdetails.std_value,
        obs_value=formdetails.obs_value,
        start_time=formdetails.start_time,
        end_time=formdetails.end_time,
        creator=formdetails.creator,
        form_name=fid,
        upload_template=tid,
        )
    template_details_values = FormDetail.objects.filter(upload_template_id=tid,form_name_id=fid).values()
    print("Template Details Count:", template_details_values.count())
    

    context={'edittemplate':template_details_values}
    return render(request,'temptoform.html',context)

def update(request):

    if request.method == 'POST':
        level_codes = request.POST.getlist('std_value[]')
        print(level_codes,'level codes')
        index_list = request.POST.getlist('id[]')
        print(index_list)
        for index, std_value in zip(index_list, level_codes):
            try:
                stddata = FormDetail.objects.get(id=int(index))
                stddata.std_value = std_value
                stddata.save()
                print(stddata,'stddaa')
            except FormDetail.DoesNotExist:
                # Handle the case where the LevelCode object with the given 'id' doesn't exist
                pass
    context = {
        'update_lc': update}

    return render(request,'updateform.html',context)


def selectform(request):
    tform=RelationTempForm
    if request.method == 'POST':
        count_form = RelationTempForm(request.POST, request.FILES)
        if count_form.is_valid():   
            count_form.save()
            return redirect('showform')
        else:
            print(count_form.errors)
    else:
        count_form = RelationTempForm()
    context = {
        'tform': tform} 
    return render(request, 'selectform.html', context)

def showform(request):
    tfr = TempFormRelation.objects.latest('id')
    tid = UploadTemplate.objects.latest('id')
    fid = UploadedForm.objects.latest('id')

    tempid=tfr.upload_template_id
    formid=tfr.form_details_id
    user=tfr.user_table_id
    print(tempid ,formid, user)

    # edittemplate=FormDetail.objects.all()
    edittemplate = FormDetail.objects.filter(upload_template_id=tid,form_name_id=fid).values()

    return render(request,'showform.html',{'edittemplate': edittemplate})

def user_check(request):
    edittemplate=FormDetail.objects.all()
    if request.method=='POST':
        return redirect('home')
    return render(request, 'userapproved.html', {'edittemplate': edittemplate})

    
    