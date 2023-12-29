from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import ExcelDataForm
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .forms import TemplateForm
import os
import pandas as pd
import pandas as pd
from .models import TemplateDetail
import numpy as np
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect



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
                    return redirect('selecttemplate')  # Superuser, redirect to the 'home' page
                else:
                    return redirect('selecttemplate')  
                
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


def home(request):
    return render(request,"home.html")


def selecttemplate(request):
    tform=TemplateForm
    if request.method == 'POST':
        count_form = TemplateForm(request.POST, request.FILES)
        if count_form.is_valid():

            count_form.save()
            # return redirect('progen')
        else:
            print(count_form.errors)
    else:
        count_form = TemplateForm()
    context = {
        'tform': tform}
    return render(request, 'tform.html', context)






def display_excel(request):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    excel_path = "static/ex.xlsx"  # Path to your Excel file

    data = pd.read_excel(excel_path)
    data = data.iloc[:, :-2]
    data = data.loc[:, ~data.columns.str.startswith('Unnamed')]
    data = data.drop(0)


    data = data.rename(columns={
        'Step': 'description',
        'Actual Readings': 'actual_readings',
        'Start Time': 'start_time',
        'End Time (hour)': 'end_time'
    })
    print(data)

    rm_col = ['Step No.', 'description', 'actual_readings', 'Unnamed: 3', 'Unnamed: 4', 'start_time', 'Unnamed: 6', 'end_time']
    sorted_data = [col for col in rm_col if not col.startswith('Unnamed')]
    
    print(sorted_data)



    for index, row in data.iterrows():
        step=1
        description = "Transfer about 50 to 60 L purified water in Tank ID TLI2M20"
        std_value = "50-60 L"
        obs_value = "0"
        start_time="0"
        end_time = "0"
        

        TemplateDetail.objects.create(
            step=step,
            description=description,
            std_value=std_value,
            obs_value=obs_value,
            start_time=start_time,
            end_time=end_time
        )
        

    # You can also query the saved data from the database and display it on the webpage
    saved_data = TemplateDetail.objects.all()
    return render(request, 'display_excel.html', {'data': data})
    

 
