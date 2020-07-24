from django.conf.urls import include, url
from django.contrib import admin
from .views import Home, success, failure

urlpatterns = [

    url('', Home),
    url('success', success),
    url('failure', failure),

]