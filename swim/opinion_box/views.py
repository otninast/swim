from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse

import json

import pandas as pd

def index(request):
    return TemplateResponse(request, 'opinion_box/index.html')


def index_ajax(request):
    try:
        df = pd.read_csv('~/Desktop/opinion_box_test.csv')
    except:
        cols = ['Time', 'Name', 'Sex', 'Themes', 'Text', 'Leng']
        df = pd.DataFrame(index=[], columns=cols)


    name = request.GET.get('name')
    sex = request.GET.get('sex')
    msg = request.GET.get('msg')
    theme = request.GET.getlist('theme[]')
    passind_time = request.GET.get('time')
    leng = len(msg)

    record = pd.Series([passind_time, name, sex, theme, msg, leng], index=df.columns)

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
