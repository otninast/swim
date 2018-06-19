from django.shortcuts import render
from django.template.response import TemplateResponse

from django.views.generic import \
    CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.views.generic import ListView


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy


from .models import Tex
from .forms import TexForm

import pandas as pd

DATA_FRAME = pd.read_csv('./assets/Result.csv')
DATA_FRAME16 = DATA_FRAME[DATA_FRAME.Competition == '16高']


class Index_View(TemplateView):
    template_name = 'testapp/index.html'

class js_Test_View(TemplateView):
    template_name = 'testapp/js_test.html'
class Camera_Test_View(TemplateView):
    template_name = 'testapp/camera_test.html'

class User_View(CreateView):
    model = User
    # fields = ('username', 'password', )
    fields = '__all__'
    template_name = 'testapp/user.html'
    # template_name = reverse_lazy('user')
    success_url = "index.html"

    # user_creation_form = UserCreationForm()
    # userlist = User.objects.all()
    # template_name = 'testapp/user.html'
    # return render(request, template_name, {'form': user_creation_form, 'user': userlist})




class Create_View(CreateView):
    model = Tex
    fields = '__all__'
    success_url = "index.html"

class List_View(ListView):
    model = Tex
    context_object_name = 'text_list'

class Detail_View(DetailView):
    model = Tex
    context_object_name = 'text'

class Delete_View(DeleteView):
    model = Tex
    success_url = reverse_lazy('list')

class Update_View(UpdateView):
    model = Tex
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})


def Chart_View(request):
    df = DATA_FRAME16
    # print('style:',df[df.Style=='fly'].shape, 'rank:', df[df.Rank=='8'].shape)
    data = df[(df.Style == 'fly') & (df.Distance == 100) & (df.Rank == '16') & (df.Sex == 'm')]
    # print('data:', data.shape)
    # label = sorted(list(set(df.Year.values)))
    # print(data.Time_sec.tolist())

    print(data.Year.unique().tolist())

    return TemplateResponse(request, 'testapp/chart.html', {'data': data.Time_sec.unique().tolist(), 'label': data.Year.unique().tolist()})
