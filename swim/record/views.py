from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse

from django.views.generic import ListView, TemplateView
from .models import Record
import json

import pandas as pd

df = pd.read_csv('/Users/tomoya/Desktop/SwimRecord/Result_all.csv')
team16 = set(df[df.Competition == '16高'].Team)


df16 = df[df.Team.isin(team16)]


#class BlogListView(ListView):
#    model = Record

def boxplot(request):
    from bokeh.charts import BoxPlot, show
    from bokeh.resources import CDN
    from bokeh.embed import components



    @interact(team=team16, sex=['m', 'w'], style=set(df16.Style), distance=sorted(set(df16.Distance)))
    def fff(team='青山', sex='m', style='fr', distance=100):
        global df16
        df16c = df16.copy()
        df16c = df16c[df16c.Team==team]
        df16c = df16c[df16c.Sex==sex]
        df16c = df16c[df16c.Style==style]
        df16c = df16c[df16c.Distance==distance]
        p = BoxPlot(df16c[['Time_sec', 'Year']])
        return show(p)



def line_plot(request):

    data_list = df[df.Style=='fr'].kyu.head(100).values
    data = [data for data in data_list]

    label = [x for x in range(1,101)]
    return TemplateResponse(request, 'record/lineplot.html',
    {'time': str(data),
    'label': str(label)})

    #return TemplateResponse(request, 'record/lineplot.html')

def ChartView(request):
    #names = set(df16[df16.Team == school].Name)
    return TemplateResponse(request, 'record/chart_view.html',
    {'school_names': list(team16)} )

    #    if request.is_ajax():

def ajax_chart(request):

    school = request.GET.get('school_name')

    names = set(df16[df16.Team == school].Name)

    dict = json.dumps({'school': school,})

    response = HttpResponse(dict, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
    #return TemplateResponse(request, 'record/chart_view.html', {'school': school })
    #return JsonResponse({'school': school})

    #def get_context_data(self):
    #    school_names = team16

        #if request.method == 'GET':

def simple_chart(request):

    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import components

    plot = figure()
    plot.circle([1,2], [3,4])

    script, div = components(plot, CDN)

    return render(request, "record/simple_chart.html", {
        "the_script": script,
        "the_div": div,
        })
