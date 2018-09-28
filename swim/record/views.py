from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import generic
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import Menue, Training, Result_Time, User_Info
from .forms import Menue_Form, Training_Form, Result_Time_Form,  Select_Form, User_Info_Form, User_Update_Form

import json
import os
from datetime import date, datetime, timedelta


import pandas as pd
from django_pandas.io import read_frame
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
sns.set()

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

from base64 import b64encode
from io import BytesIO

PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'Result_all.csv'))
# PATH = os.path.join(os.path.dirname(__file__), 'Result_all.csv')
Df = pd.read_csv(PATH)
Team16 = set(Df[Df.Competition == '16高'].Team)
Df16 = Df[Df.Team.isin(Team16)]


def new(request):
    form = UserCreationForm()
    user_info_form = User_Info_Form()
    context = {'form': form, 'user_info_form': user_info_form}
    return TemplateResponse(request, 'record/new.html', context)
def create(request):
    form = UserCreationForm()
    user_info_form = User_Info_Form()
    context = {'form': form, 'user_info_form': user_info_form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user_info_form = User_Info_Form(request.POST)
        if form.is_valid():
            form.save()
            user_info_form.save()
            return redirect('login.html')
        else:
            return render(request, 'record/new.html', context)
    else:
        return Http404

@login_required
def Index(request):
    user_info_form = User_Info_Form()

    end_w = date.today()
    start_w = end_w - timedelta(days = 7)

    end_m = date.today()
    start_m = end_m - timedelta(days = 30)

    # timelist_week = Result_Time.objects.filter(training__date__range=(start_w, end_w))
    # timelist_month = Result_Time.objects.filter(training__date__range=(start_m, end_m))
    timelist_week = Result_Time.objects.filter(training__user__exact=request.user).filter(training__date__range=(start_w, end_w))
    timelist_month = Result_Time.objects.filter(training__user__exact=request.user).filter(training__date__range=(start_m, end_m))

    context = {'timelist_week':timelist_week,
                'timelist_month': timelist_month,
                'user_info_form': user_info_form,
                # 'user': request.user,
                }
    return TemplateResponse(request, 'record/index.html', context)

@login_required
def Player_List(request):
    player_list = User.objects.all()
    context = {'player_list': player_list}
    return render(request, 'record/player_list.html', context)

class Player_Info(generic.DetailView):
    model = User
    template_name = 'record/player.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = Result_Time.objects.all()
        context['time_user'] = Result_Time.objects.filter(training__user__exact=self.request.user)
        df = read_frame(context['time_user'])
        context['img_tag'] = make_img(df.second)
        # print(df)
        # for k in context['time_user']:
        #     print(k)

        return context

class Player_Update(generic.UpdateView):
    model = User_Info
    # form_class = UserChangeForm
    form_class = User_Info_Form
    # fields = '__all__'
    template_name = 'record/player_update.html'
    def get_success_url(self):
        return reverse_lazy('player_info', kwargs={'pk': self.kwargs['pk']})



@login_required
def OpinionBox(request):
    path_to_opinion = os.path.join(os.path.join(os.path.dirname(__file__), 'opinion_box.csv'))
    try:
        os.remove(path_to_opinion)
    except:
        print('ありません')
    return TemplateResponse(request, 'record/opinion_box.html')
def OpinionBoxAjax(request):
    try:
        df = pd.read_csv(path_to_opinion)
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
    df.to_csv(path_to_opinion, index=False)



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
        df = pd.read_csv(path_to_opinion)


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

    if request.method == 'POST':
        m_10_ = [int(i) for i in request.POST.getlist('m_10')]
        m_1_ = [int(i) for i in request.POST.getlist('m_1')]
        s_10_ = [int(i) for i in request.POST.getlist('s_10')]
        s_1_ = [int(i) for i in request.POST.getlist('s_1')]
        ms_10_ = [int(i) for i in request.POST.getlist('ms_10')]
        ms_1_ = [int(i) for i in request.POST.getlist('ms_1')]

        form = Training_Form(request.POST)

        if form.is_valid():
            #form.save()...modelインスタンス生成
            #model.userに直接user情報を入れる
            #model.save()
            training = form.save(commit=False)
            training.user = request.user
            training.save()

            for index, (m_10, m_1, s_10, s_1, ms_10, ms_1) in enumerate(zip(m_10_, m_1_, s_10_, s_1_, ms_10_, ms_1_)):
                result = Result_Time(training=training)
                result.second = 60*(10*m_10 + m_1)+(10*s_10 + s_1)+(10*float(ms_10) + float(ms_1))/100
                result.num_of_swim = index+1
                result.time_str = '{}{}:{}{}.{}{}'.format(m_10, m_1, s_10, s_1, ms_10, ms_1)
                result.save()

            return redirect(reverse_lazy('index'))

        else:
            return HttpResponseRedirect('record/input_data.html', {'form': form, 'form2': form2})
    else:
        form = Training_Form()
        form2 = Result_Time_Form()
        return TemplateResponse(request, 'record/input_data.html', {'form': form, 'form2': form2})


@login_required
def ChartView(request):
    select_form = Select_Form()
    return TemplateResponse(request, 'record/chart_view.html',
                            {'school_names': sorted(list(Team16)),
                            'select_form': select_form
                            })

def ajax_chart(request):
    schools = request.GET.get('school_name').replace("'", "")
    years = request.GET.get('year').replace("'", "")
    styles = request.GET.get('style').replace("'", "")
    distances = request.GET.get('distance').replace("'", "")
    sexs = request.GET.get('sex').replace("'", "")

    print(type(years), years)

    school = schools[1:-1].replace(' ', '').split(',') if schools[0]=='[' else [schools]
    year = years[1:-1].replace(' ', '').split(',') if years[0]=='[' else [years]
    style = styles[1:-1].replace(' ', '').split(',') if styles[0]=='[' else [styles]
    distance = distances[1:-1].replace(' ', '').split(',') if distances[0]=='[' else [distances]
    sex = sexs[1:-1].replace(' ', '').split(',') if sexs[0]=='[' else [sexs]

    print(type(year), year)
    print(type(year[0]), year[0])

    col=['Name', 'Age', 'Sex', 'Style', 'Distance', 'Time', 'Rank', 'kyu']

    try:
        dfa = Df[Df.Competition == '16高']

        dfc = dfa[(dfa.Team.isin(school))&
        (dfa.Year.isin(year))&
        (dfa.Style.isin(style))&
        (dfa.Distance.isin(distance))&
        (dfa.Sex.isin(sex))]

        table = dfc.to_html(index=False)
        # print('##########1111#############')

        fig, ax = plt.subplots()
        ax = sns.boxplot(dfc.Year, dfc.kyu, hue='Sex', data=dfc)
        canvas = FigureCanvasAgg(fig)
        # print('#########2222##############')

        png_output = BytesIO()
        canvas.print_png(png_output)
        bs64 = b64encode(png_output.getvalue())
        image = str(bs64)
        image = image[2:-1]
        # print('#########33333##############')

        # table = dfa[(dfa.Year==2009)&(dfa.Competition=='16高')][col].to_html(index=False)
        table = dfc[col].to_html(index=False)

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


def Test(request):
    return render(request, 'record/test.html')


def make_img(df):
    fig, ax = plt.subplots()
    ax = df.plot()
    canvas = FigureCanvasAgg(fig)

    png_output = BytesIO()
    canvas.print_png(png_output)
    bs64 = b64encode(png_output.getvalue())
    image = str(bs64)
    image = image[2:-1]

    # img_tag = "<img src='data:image/png;base64," + image + "/>"
    # img_tag = "<img src='data:image/png;base64,{}>".format(image)
    img_tag = 'data:image/png;base64,{}'.format(image)

    return img_tag
