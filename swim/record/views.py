from django.urls import reverse_lazy
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Person, Menue, Time_Result
from .forms import Menue_Form, Time_Result_Form

import json
import os

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
    form = UserCreationForm()
    return TemplateResponse(request, 'record/new.html', {'form': form,})
def create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('login.html')
        else:
            return TemplateResponse(request, 'record/new.html', {'form': form,})
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

@login_required
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

@login_required
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
    menue_form = Menue_Form()
    time_result_form = Time_Result_Form()
    return TemplateResponse(request, 'record/input_data.html', {'menue_form': menue_form, 'time_result_form': time_result_form})


def ChartView(request):
    #names = set(df16[df16.Team == school].Name)
    return TemplateResponse(request, 'record/chart_view.html',
                            {'school_names': list(Team16)})
def ajax_chart(request):
    school = request.GET.get('school_name')

    dfa=Df[Df.Team==school]

    fig, ax = plt.subplots()
    ax = sns.boxplot(dfa.Year, dfa.kyu, hue='Sex', data=dfa)
    canvas = FigureCanvasAgg(fig)
    # response = HttpResponse(content_type='image/png')
    # canvas.print_png(response)

    png_output = BytesIO()
    canvas.print_png(png_output)
    bs64 = b64encode(png_output.getvalue())
    image = str(bs64)
    image = image[2:-1]

    dict = json.dumps({'school': school, 'image': image})

    response = HttpResponse(dict, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response



"""
def boxplot(request):
    from bokeh.charts import BoxPlot, show
    from bokeh.resources import CDN
    from bokeh.embed import components

    @interact(team=team16, sex=['m', 'w'], style=set(df16.Style), distance=sorted(set(df16.Distance)))
    def fff(team='青山', sex='m', style='fr', distance=100):
        global df16
        df16c = df16.copy()
        df16c = df16c[df16c.Team == team]
        df16c = df16c[df16c.Sex == sex]
        df16c = df16c[df16c.Style == style]
        df16c = df16c[df16c.Distance == distance]
        p = BoxPlot(df16c[['Time_sec', 'Year']])
        return show(p)
def line_plot(request):

    data_list = df[df.Style == 'fr'].kyu.head(100).values
    data = [data for data in data_list]

    label = [x for x in range(1, 101)]
    return TemplateResponse(request, 'record/lineplot.html',
                            {'time': str(data),
                             'label': str(label)})

    # return TemplateResponse(request, 'record/lineplot.html')
def simple_chart(request):

    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components

    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot, CDN)

    return render(request, "record/simple_chart.html", {
        "the_script": script,
        "the_div": div,
    })
"""
