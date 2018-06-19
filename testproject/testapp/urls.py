from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index', views.Index_View.as_view(), name='index'),
    url(r'^create', views.Create_View.as_view(), name='create'),
    url(r'^list', views.List_View.as_view(), name='list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.Detail_View.as_view(), name='detail'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.Delete_View.as_view(), name='delete'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.Update_View.as_view(), name='update'),


    url(r'^chart', views.Chart_View, name='chart'),
    url(r'^js_test', views.js_Test_View.as_view(), name='js_test'),
    url(r'^camera_test', views.Camera_Test_View.as_view(), name='camera_test'),
    url(r'^user', views.User_View.as_view(), name='user'),

]
