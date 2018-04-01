from django.conf.urls import url

from . import views
#from record.views import ChartView

urlpatterns = [
    url(r'^simple_chart/$', views.simple_chart, name='simple_chart'),
    #path('', BlogListView.as_view(), name='index'),
    url(r'^lineplot/$',views.line_plot, name='lineplot'),
    url(r'^chart/$', views.ChartView, name='chart_view'),
    url(r'^ajax_chart/', views.ajax_chart, name='ajax_chart'),
    #url(r'chart/$', views.chart, name='chart'),
]
