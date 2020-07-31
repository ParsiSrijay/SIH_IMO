from django.shortcuts import render,redirect
from django.http import HttpResponse
from addshg.models import shg,Loan
from django.db.models import Avg, Count, Min, Sum,Max
from django.db.models.functions import ExtractMonth

# Create your views here.

def home(request):
    return render(request,'a/themexriver.com/tfhtml/finance-top/index.html')

def activity(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    l=[]
    lm=[0]*12
    lact = []
    for i in range(7):
        lact.append([])
        for j in range(12):
            lact[i].append(0)
    dict_act={}
    dates=Loan.objects.all().annotate(order_month=ExtractMonth('Date'))
    for i in dates:
        lm[i.order_month-1]=i.LoanRepayment+lm[i.order_month-1]
        act=shg.objects.values("Activity").filter(Registration_id_imo=request.user.username,Name=i.Name)[0]
        if act['Activity']=="Tailoring":
            lact[0][i.order_month-1]=i.LoanRepayment+lact[0][i.order_month-1]
        if act['Activity']=="Handicraft":
            lact[1][i.order_month-1]=i.LoanRepayment+lact[1][i.order_month-1]
        if act['Activity']=="Handloom":
            lact[2][i.order_month-1]=i.LoanRepayment+lact[2][i.order_month-1]
        if act['Activity']=="Agriculture":
            lact[3][i.order_month-1]=i.LoanRepayment+lact[3][i.order_month-1]
        if act['Activity']=="Diary Activities":
            lact[4][i.order_month-1]=i.LoanRepayment+lact[4][i.order_month-1]
        if act['Activity']=="Food Processing":
            lact[5][i.order_month-1]=i.LoanRepayment+lact[5][i.order_month-1]
        if act['Activity']=="Others":
            lact[6][i.order_month-1]=i.LoanRepayment+lact[6][i.order_month-1]
    print(lact)
    act=shg.objects.values("Activity").filter(Registration_id_imo=request.user.username)
    for i in act:
        if i['Activity'] not in l:
            l.append(i['Activity'])
    l2=[]
    l3=[]
    for i in range(len(l)):
        act_income=shg.objects.filter(Registration_id_imo=request.user.username,Activity=l[i]).aggregate(s=Sum('Amount'),t=Sum('BalanceAmount'))
        l2.append(act_income['s'])
        l3.append(act_income['t'])
    l4=[]
    for i in range(len(l)):
        dict={}
        dict['Activity']=l[i]
        dict['Income']=l2[i]-l3[i]
        l4.append(dict)
    return render(request,'chart.html',{'dest1' :l4,"list1":lm,"lact0":lact[0],"lact1":lact[1],"lact2":lact[2],"lact3":lact[3],"lact4":lact[4],"lact5":lact[5],"lact6":lact[6] })
