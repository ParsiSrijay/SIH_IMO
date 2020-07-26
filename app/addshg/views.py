
from django.shortcuts import render,redirect
import joblib
import numpy as np
from addshg.models import shg,installments,Loan


def signup(request):
        if not request.user.is_authenticated:
            return redirect('http://127.0.0.1:8000/login')
        if request.method == 'POST':
            name=request.POST['name']
            act=request.POST['act']
            amount=request.POST['amt']
            amt=int(amount)*100000
            woman=request.POST['wb']
            location=request.POST['location']
            tp=request.POST['tp']
            rate=request.POST['rate']
            reg=request.POST['reg']
            pd=request.POST['pd']
            ycj=request.POST['ycj']
            action=act
            if pd=='Yes' or pd=='yes' or pd=='y':
                pd=1
            else:
                pd=0
            if act=='Tailoring':
                act=1
            elif act=='Handicraft':
                act=2
            elif act=='Handloom':
                act=3
            elif act=='Agriculture':
                act=4
            elif act=='Diary Activities':
                act=5
            elif act == 'Food Processing':
                act = 6
            else:
                act=7
                action="Fishing"
            model = joblib.load('C:/Users/P SRIJAY/Desktop/sih/imo1.pkl')
            x=[int(amount),int(woman),int(ycj),int(tp),act,pd]
            x=np.array(x)
            x=x.reshape(1,-1)
            y_test=model.predict(x)
            if y_test[0]==1:
                s=shg(Name=name,Activity=action,Amount=amt,Woman_beneficiaries=woman,Location=location,TimePeriod=tp,Rate=rate,Registration_id_imo=request.user.username)
                s.save()
                lr = Loan(Name=name, OpeningBalance=amt, LoanRepayment=0, Interest=0, ClosingBalance=amt,RegIMO=request.user.username)
                lr.save()
                return render(request,'approveSHG.html',{'content':"Loan Approved Successfully!"})
            else:
                return render(request,'approveSHG.html',{'content': "Loan Rejected!!"})
        else:
            return render(request,'approveSHG.html',{"reg":request.user.username})


def display(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    list_shg=shg.objects.values('Name','Amount','Activity').filter(Registration_id_imo=request.user.username)
    return render(request,"displaySHG.html",{'shg':list_shg})


def payinstallments(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    if request.method=='POST':
        id=request.POST['id']
        name=request.POST['name']
        inst=request.POST['installments']
        reg=request.POST['reg']
        s=shg.objects.get(Name=name,Registration_id_imo=reg)
        openbal=s.Amount
        loaninst=inst
        rate=s.Rate/12
        time=s.TimePeriod
        interest= (openbal*rate*time)/100
        closebal=openbal-int(loaninst)+interest
        s.Amount=closebal
        s.save()
        t = installments(Name=name, Installments=int(inst), Registration_id_imo=request.user.username)
        t.save()
        lr=Loan(Name=name,OpeningBalance=openbal,LoanRepayment=inst,Interest=interest,ClosingBalance=closebal,RegIMO=request.user.username)
        lr.save()
        return redirect('http://127.0.0.1:8000/portal/display')
    else:
        return render(request,'installments.html',{"reg":request.user.username})

def dispLR(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    name_list = Loan.objects.raw('SELECT DISTINCT Name,id from addshg_loan WHERE RegIMO=%s',[request.user.username])
    l = []
    for i in name_list:
        if i.Name not in l:
            l.append(i.Name)
    if request.method=="POST":
        name=request.POST['name']
        lr=Loan.objects.all().filter(Name=name,RegIMO=request.user.username)
        return render(request,"form.html",{"shg":lr,"name_list":l})
    else:
        return render(request,"form.html",{"name_list":l})
