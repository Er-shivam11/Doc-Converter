from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render
from .forms import ExcelDataForm
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import UserPermissionForm,UploadWorkSheetForm
import os
import pandas as pd
from .models import TemplateDetail,UploadTemplate
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
            # Save the form
            upload_template_instance = form.save()

            # Read the Excel file using pandas
            try:
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
                # print(data)
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
                        step = 1
                # Create an instance of the TemplateDetail model and save it to the database
                    TemplateDetail.objects.create(
                        step=step,
                        description=description,
                        std_value=std_value,
                        obs_value=obs_value,
                        start_time=start_time,
                        end_time=end_time,
                        creator=creator_name

                    )
                
                # Print the values

            except pd.errors.EmptyDataError:
                print("The Excel file is empty.")
            
            return redirect('selecttemplate')
        else:
            # Handle form errors - you can print them or log them for debugging
            print(form.errors)

    name=UploadTemplate.objects.all()
    print('name',name)

    context = {
        'form': form
    }
    return render(request, 'newform.html', context)



def home(request):
    return render(request,"home.html")

def selecttemplate(request):
    tform=UserPermissionForm
    if request.method == 'POST':
        count_form = UserPermissionForm(request.POST, request.FILES)
        if count_form.is_valid():

            count_form.save()
            return redirect('editform')
        else:
            print(count_form.errors)
    else:
        count_form = UserPermissionForm()
    context = {
        'tform': tform}
    return render(request, 'tform.html', context)

def edit(request):
    edittemplate=TemplateDetail.objects.all()

    context={'edittemplate':edittemplate}
    return render(request,'display_form.html',context)

def update(request):
    if request.method == 'POST':
        # Assuming you have a unique identifier for each TemplateDetail instance
        # For example, let's assume 'id' is the primary key
        template_detail_id = request.POST.get('id')
        
        # Retrieve the TemplateDetail instance from the database
        template_detail = TemplateDetail.objects.get(id=template_detail_id)

        # Update the std_value field with the form data
        template_detail.std_value = request.POST.get('std_value')

        # Save the updated instance back to the database
        template_detail.save()

        # Redirect to a success page or wherever you want to go after saving
        return redirect('success_page')
    edittemplate=TemplateDetail.objects.all()

    return render(request,'update.html',{'edittemplate': edittemplate})

def user_check(request):
    
    edittemplate=TemplateDetail.objects.all()

    # Handle GET requests or any other logic here
    # ...

    # Render the template with the form
    return render(request, 'userapproved.html', {'edittemplate': edittemplate})

    
    