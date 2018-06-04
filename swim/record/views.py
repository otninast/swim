# from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
# from django.views import View
# from django.views.generic import ListView, TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Menue, Training, Result_Time
from .forms import Menue_Form, Training_Form, Result_Time_Form,  Select_Form

import json
import os
from datetime import date

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
sns.set()

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

from base64 import b64encode
from io import BytesIO


Df = pd.read_csv('~/swimrecord/swim/record/Result_all.csv')
Team16 = set(Df[Df.Competition == '16高'].Team)
Df16 = Df[Df.Team.isin(Team16)]


def new(request):
    # form = UserCreationForm()
    form = UserCreationForm()
    return TemplateResponse(request, 'record/new.html', {'form': form,})
def create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # pass
            return redirect('login.html')
        else:
            return render(request, 'record/new.html', {'form': form,})
    else:
        return Http404

@login_required
def Index(request):
    return TemplateResponse(request, 'record/index.html')


@login_required
def OpinionBox(request):
    try:
        os.remove('/Users/tomoya/Desktop/opinion_box_test.csv')
    except:
        print('ありません')
    return TemplateResponse(request, 'record/opinion_box.html')
def OpinionBoxAjax(request):
    try:
        df = pd.read_csv('~/Desktop/opinion_box_test.csv')
    except:
        cols = ['Index','Time', 'Name', 'Sex', 'Themes', 'Text', 'Leng']
        df = pd.DataFrame(index=[], columns=cols)

    index = request.GET.get('index')
    name = request.GET.get('name')
    sex = request.GET.get('sex')
    msg = request.GET.get('msg')
    theme = request.GET.getlist('theme[]')
    passind_time = request.GET.get('time')
    leng = len(msg)

    record = pd.Series([index, passind_time, name, sex, theme, msg, leng], index=df.columns)

    df = df.append(record, ignore_index=True)
    df.to_csv('~/Desktop/opinion_box_test.csv', index=False)



    dict = json.dumps({'name': name,
                        'sex': sex,
                        'leng': leng,
                        'theme': theme})

    response = HttpResponse(dict, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response
def OpinionBoxResult(request):
        df = pd.read_csv('~/Desktop/opinion_box_test.csv')


        fig, ax = plt.subplots()
        ax = df.Leng.plot()
        canvas = FigureCanvasAgg(fig)

        png_output = BytesIO()
        canvas.print_png(png_output)
        bs64 = b64encode(png_output.getvalue())
        image = str(bs64)
        image = image[2:-1]

        dict = json.dumps({'image': image})

        response = HttpResponse(dict, content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response


@login_required
def Input_Data(request):
    form = Training_Form()
    form2 = Result_Time_Form()
    if request.method == 'POST':

        t_min = request.POST.getlist('time_minutes')
        t_sec = request.POST.getlist('time_seconds')
        t_mic = request.POST.getlist('time_seconds_micro')

        form = Training_Form(request.POST)

        if form.is_valid():
            form.save()

            for minute, second, micro in zip(t_min, t_sec, t_mic):
                # training_id = Training.objects.get
                result = Result_Time()
                result.time_minutes = minute
                result.time_seconds = second
                result.time_seconds_micro = micro
                result.save()

            return HttpResponse(request, 'record/index.html')

        else:
            return HttpResponseRedirect('record/input_data.html', {'form': form, 'form2': form2})
    else:

        return TemplateResponse(request, 'record/input_data.html', {'form': form, 'form2': form2})


@login_required
def ChartView(request):
    select_form = Select_Form()
    return TemplateResponse(request, 'record/chart_view.html',
                            {'school_names': sorted(list(Team16)),
                            'select_form': select_form

                            })
def ajax_chart(request):
    # school = []
    # year = []
    # style=[]
    # distance=[]
    # sex=[]

    schools = request.GET.get('school_name').replace("'", "")
    years = request.GET.get('year').replace("'", "")
    styles = request.GET.get('style').replace("'", "")
    distances = request.GET.get('distance').replace("'", "")
    sexs = request.GET.get('sex').replace("'", "")

    # print(schools)
    # print(type(schools))
    # print('sexs', sexs, type(sexs))

    school = schools[1:-1].replace(' ', '').split(',') if schools[0]=='[' else [schools]
    year = years[1:-1].replace(' ', '').split(',') if years[0]=='[' else [years]
    style = styles[1:-1].replace(' ', '').split(',') if styles[0]=='[' else [styles]
    distance = distances[1:-1].replace(' ', '').split(',') if distances[0]=='[' else [distances]
    sex = sexs[1:-1].replace(' ', '').split(',') if sexs[0]=='[' else [sexs]

    # school = schools if type(schools)==list else [schools]
    # year = years if type(years)==list else [years]
    # style = styles if type(styles)==list else [styles]
    # distance = distances if type(distances)==list else [distances]
    # sex = sexs if type(sexs)==list else [sexs]

    # [school.append(x) for x in [schools]]
    # [year.append(x) for x in years]
    # [style.append(x) for x in [styles]]
    # [distance.append(x) for x in [distances]]
    # [sex.append(x) for x in sexs]
    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print(type(years), type(distances), years, distances, sexs, styles)
    # print(type(year), type(distance), year, distance, sex, style)

    col=['Name', 'Age', 'Sex', 'Style', 'Distance', 'Time', 'Rank', 'kyu']

    try:
        dfa = Df[Df.Competition == '16高']
        # print(dfa.head())
        dfa = dfa[(dfa.Team.isin(school))&
        (dfa.Year.isin(year))&
        (dfa.Style.isin(style))&
        (dfa.Distance.isin(distance))&
        (dfa.Sex.isin(sex))]

        table = dfa.to_html(index=False)
        # print('##########1111#############')
        # print(dfa.head())

        fig, ax = plt.subplots()
        ax = sns.boxplot(dfa.Year, dfa.kyu, hue='Sex', data=dfa)
        canvas = FigureCanvasAgg(fig)
        # print('#########2222##############')

        png_output = BytesIO()
        canvas.print_png(png_output)
        bs64 = b64encode(png_output.getvalue())
        image = str(bs64)
        image = image[2:-1]
        # print('#########33333##############')

        # table = dfa[(dfa.Year==2009)&(dfa.Competition=='16高')][col].to_html(index=False)
        table = dfa[col].to_html(index=False)

        dict = json.dumps({'school': school, 'image': image, 'table': table})

        response = HttpResponse(dict, content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    except:
        dict = json.dumps({'table':'No Data...'})
        return HttpResponse(dict)
