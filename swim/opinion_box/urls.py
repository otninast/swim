from django.conf.urls import url

from . import views
#from record.views import ChartView

urlpatterns = [
    url(r'^index/$', views.index, name='index2'),
    url(r'^index_ajax/', views.index_ajax, name='index_ajax'),
    # url(r'^index.css/'),

]
