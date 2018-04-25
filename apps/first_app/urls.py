from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^create$', views.create),
    url(r'^remove/(?P<number>\d+)$', views.remove),
    url(r'^users/(?P<number>\d+)$', views.show),
    url(r'^add/(?P<number>\d+)$', views.add),
]
