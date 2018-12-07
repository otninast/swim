from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import DayMenu, TrainingMenu, Result_Time, User_Info
from .forms import DayMenu_Form, TrainingMenu_Form, Result_Time_Form, Select_Form, User_Info_Form

import json
import os
from datetime import date, timedelta


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

    timelist_week = Result_Time.objects.filter(trainingmenu__daymenu__user__exact=request.user).filter(trainingmenu__daymenu__date__range=(start_w, end_w))
    timelist_month = Result_Time.objects.filter(trainingmenu__daymenu__user__exact=request.user).filter(trainingmenu__daymenu__date__range=(start_m, end_m))

    context = {'timelist_week':timelist_week,
                'timelist_month': timelist_month,
                'user_info_form': user_info_form,
                'username': str(request.user),
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

        return context


class Player_Update(generic.UpdateView):
    model = User_Info
    form_class = User_Info_Form
    template_name = 'record/player_update.html'

    def get_success_url(self):
        return reverse_lazy('player_info', kwargs={'pk': self.kwargs['pk']})


@login_required
def Input_Data(request):

    if request.method == 'POST':
        m_10_ = [int(i) for i in request.POST.getlist('m_10')]
        m_1_ = [int(i) for i in request.POST.getlist('m_1')]
        s_10_ = [int(i) for i in request.POST.getlist('s_10')]
        s_1_ = [int(i) for i in request.POST.getlist('s_1')]
        ms_10_ = [int(i) for i in request.POST.getlist('ms_10')]
        ms_1_ = [int(i) for i in request.POST.getlist('ms_1')]

        daymenu_form = DayMenu_Form(data=request.POST)
        trainingmenu_form = TrainingMenu_Form(data=request.POST)

        if daymenu_form.is_valid() and trainingmenu_form.is_valid():
            training = trainingmenu_form.save(commit=False)
            daymenu = daymenu_form.save(commit=False)
            daymenu.user = request.user
            daymenu.save()
            training.daymenu = daymenu
            print(training.daymenu, daymenu)
            training.save()

            for index, (m_10, m_1, s_10, s_1, ms_10, ms_1) in enumerate(zip(m_10_, m_1_, s_10_, s_1_, ms_10_, ms_1_)):
                result = Result_Time(trainingmenu=training)
                result.time = 60*(10*m_10 + m_1)+(10*s_10 + s_1)+(10*float(ms_10) + float(ms_1))/100
                result.order = index+1
                result.time_str = '{}{}:{}{}.{}{}'.format(m_10, m_1, s_10, s_1, ms_10, ms_1)
                result.save()

            print('成功')
            return redirect(reverse_lazy('index'))

        else:
            print('失敗')
            return redirect(reverse_lazy('index'))

    else:
        daymenu_form = DayMenu_Form()
        trainingmenu_form = TrainingMenu_Form()
        result_time_form = Result_Time_Form()
        rap_time_form = Rap_Time_Form()
        return TemplateResponse(request, 'record/input_data.html',
                    {'daymenu_form': daymenu_form,
                    'trainingmenu_form': trainingmenu_form,
                    'result_time_form': result_time_form,
                    'rap_time_form': rap_time_form})


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

    school = schools[1:-1].replace(' ', '').split(',') if schools[0]=='[' else [schools]
    year = years[1:-1].replace(' ', '').split(',') if years[0]=='[' else [years]
    style = styles[1:-1].replace(' ', '').split(',') if styles[0]=='[' else [styles]
    distance = distances[1:-1].replace(' ', '').split(',') if distances[0]=='[' else [distances]
    sex = sexs[1:-1].replace(' ', '').split(',') if sexs[0]=='[' else [sexs]
    col = ['Name', 'Age', 'Sex', 'Style', 'Distance', 'Time', 'Rank', 'kyu']

    try:
        dfa = Df[Df.Competition == '16高']

        dfc = dfa[(dfa.Team.isin(school)) &
                    (dfa.Year.isin(year)) &
                    (dfa.Style.isin(style)) &
                    (dfa.Distance.isin(distance)) &
                    (dfa.Sex.isin(sex))]

        table = dfc.to_html(index=False)

        fig, ax = plt.subplots()
        ax = sns.boxplot(dfc.Year, dfc.kyu, hue='Sex', data=dfc)
        canvas = FigureCanvasAgg(fig)

        png_output = BytesIO()
        canvas.print_png(png_output)
        bs64 = b64encode(png_output.getvalue())
        image = str(bs64)
        image = image[2:-1]

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


def make_img(df):
    fig, ax = plt.subplots()
    ax = df.plot()
    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    bs64 = b64encode(png_output.getvalue())
    image = str(bs64)
    image = image[2:-1]
    img_tag = 'data:image/png;base64,{}'.format(image)

    return img_tag


class TopPage(generic.ListView, ModelFormMixin):
    model = DayMenu
    fields = '__all__'
    # context_object_name = 'request_users_daymenus'
    success_url = reverse_lazy('top')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = DayMenu.objects.filter(user=self.request.user).order_by('-date')
        # xx = data[2].trainingmenus.all()[0].times.all()
        # xxx = [xx[i].time for i in range(len(xx))]
        # df = pd.DataFrame(data=xxx)
        # df = read_frame(context['time_user'])

        context['request_users_daymenus'] = data
        # context['img'] = make_img(df)
        daymenu_form = DayMenu_Form()
        trainingmenu_form = TrainingMenu_Form()
        result_time_form = Result_Time_Form()

        context['daymenu_form'] = daymenu_form
        context['trainingmenu_form'] = trainingmenu_form
        context['result_time_form'] = result_time_form

        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()
        # if form.is_valid():
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)
        input(request)
        print(self.form_valid(form))
        return self.form_valid(form)


class Training_Detail(generic.DetailView):
    model = DayMenu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        training = TrainingMenu.objects.filter(daymenu=obj)
        context['training'] = training
        return context



def input(request):

    m_10_ = [int(i) for i in request.POST.getlist('m_10')]
    m_1_ = [int(i) for i in request.POST.getlist('m_1')]
    s_10_ = [int(i) for i in request.POST.getlist('s_10')]
    s_1_ = [int(i) for i in request.POST.getlist('s_1')]
    ms_10_ = [int(i) for i in request.POST.getlist('ms_10')]
    ms_1_ = [int(i) for i in request.POST.getlist('ms_1')]

    daymenu_form = DayMenu_Form(data=request.POST)
    trainingmenu_form = TrainingMenu_Form(data=request.POST)

    if daymenu_form.is_valid() and trainingmenu_form.is_valid():
        training = trainingmenu_form.save(commit=False)
        daymenu = daymenu_form.save(commit=False)
        daymenu.user = request.user
        daymenu.save()
        training.daymenu = daymenu
        training.save()

        for index, (m_10, m_1, s_10, s_1, ms_10, ms_1) in enumerate(zip(m_10_, m_1_, s_10_, s_1_, ms_10_, ms_1_)):
            result = Result_Time(trainingmenu=training)
            result.time = 60*(10*m_10 + m_1)+(10*s_10 + s_1)+(10*float(ms_10) + float(ms_1))/100
            result.order = index+1
            result.time_str = '{}{}:{}{}.{}{}'.format(m_10, m_1, s_10, s_1, ms_10, ms_1)
            result.save()


        return redirect(reverse_lazy('index'))

    else:

        return redirect(reverse_lazy('index'))

def bokeh_graph(data):
    from bokeh.plotting import figure
    # from bokeh.transform import jitter
    from bokeh.embed import components

    p = figure()
    p.line(data.index, data.distance, color='red')

    script, div = components(p)
    return script, div
