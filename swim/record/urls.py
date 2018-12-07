from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from . import views


# app_name = 'record'

urlpatterns = [
    url(r'^login', LoginView.as_view(template_name='record/login.html'), name='login'),
    url(r'^logout', LogoutView.as_view(template_name='record/logout.html'), name='logout'),

    url(r'^new', views.new, name='new'),
    url(r'^create', views.create, name='create'),

    url(r'^$', views.Index, name='index'),

    url(r'^input_data/$', views.Input_Data, name='input_data'),

    url(r'^ajax_chart/', views.ajax_chart, name='ajax_chart'),
    url(r'^chart/$', views.ChartView, name='chart_view'),

    url(r'^player_list/$', views.Player_List, name='player_list'),
    url(r'^player/(?P<pk>[0-9]+)/$', views.Player_Info.as_view(), name='player_info'),
    url(r'^player_update/(?P<pk>[0-9]+)/$', views.Player_Update.as_view(), name='player_update'),


    url(r'^top/$', views.TopPage.as_view(), name='top'),
    url(r'^top/(?P<pk>[0-9]+)/$', views.Training_Detail.as_view(), name='detail'),
]
