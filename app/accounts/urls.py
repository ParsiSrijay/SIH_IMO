from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.first,name ='first'),
    path('display',views.disp,name="display")
]
