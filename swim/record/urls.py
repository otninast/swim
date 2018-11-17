from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

#from record.views import ChartView
# app_name = 'record'

urlpatterns = [
    # url(r'^simple_chart/$', views.simple_chart, name='simple_chart'),
    # url(r'^lineplot/$', views.line_plot, name='li'),
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
    # url(r'^player_update/(?P<pk>[0-9]+)/$', views.Player_Update, name='player_update'),

    # path(r'^player/<int:pk>/', views.Player_Info, name='player_info'),

    # url(r'^opinion_box/$', views.OpinionBox, name='opinion_box'),
    # url(r'^opinion_box_ajax/$', views.OpinionBoxAjax, name='opinion_box_ajax'),
    # url(r'^opinion_box_result/$', views.OpinionBoxResult, name='opinion_box_result'),

    # url(r'^test/$', views.Test, name='test'),

]
