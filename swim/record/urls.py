from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from . import views

#from record.views import ChartView

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

    url(r'^opinion_box/$', views.OpinionBox, name='opinion_box'),
    url(r'^opinion_box_ajax/$', views.OpinionBoxAjax, name='opinion_box_ajax'),
    url(r'^opinion_box_result/$', views.OpinionBoxResult, name='opinion_box_result'),


    #path('', BlogListView.as_view(), name='index'),
    #url(r'chart/$', views.chart, name='chart'),
]
