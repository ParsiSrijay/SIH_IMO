from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.FinRecords,name ='fr'),
    path("first",views.first,name='first'),
    path('display',views.disp,name="display"),
    path('edit',views.edit,name="edit"),
    path('receipt/',views.receipts,name='receipts'),
    path('receipt/display',views.RandPDisplay,name="r&pd"),
    path('iedisp',views.IandEDisplay,name="iande"),
    path('balsheet',views.BalanceSheet,name="bs"),
    path('cashAcc',views.CashAccountDisp,name="cs"),
]
