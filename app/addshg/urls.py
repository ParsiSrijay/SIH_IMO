from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.signup,name ='signup'),
    path('display',views.display,name='display'),
    path('install',views.payinstallments,name='install'),
    path('dispLR',views.dispLR,name='dispLR')
]
