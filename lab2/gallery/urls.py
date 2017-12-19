from django.conf.urls import url
from gallery import views

urlpatterns = [
    url(r'^$', views.hello, name="hello"),
    url(r'^hello/$', views.hello, name="hello"),
    url(r'^showfacts/$', views.showfacts, name="showfacts"),
    url(r'^update/$', views.update, name="update"),
    url(r'^visitors/$', views.visitors, name="visitors")
]
