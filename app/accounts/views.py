from django.shortcuts import render,redirect
from .models import ledger
from django.db.models import Avg, Count, Min, Sum
# Create your views here.
def first(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    if(request.method=="POST"):
        account_name=request.POST['account']
        transctionType=request.POST['TransctionType']
        particulars=request.POST['particulars']
        amount=request.POST['amount']
        if account_name=="" or particulars=="" or amount==0:
            return render(request,'ledger.html',{"failure":"All the fields need to be entered"})
        l = ledger(AccountName=account_name,TransctionType=transctionType,Particulars=particulars,Amount=amount)
        l.save()
        if transctionType=="Debit":
            l1=ledger(AccountName=particulars,TransctionType="Credit",Particulars=account_name,Amount=amount)
            l1.save()
        else:
            l1 = ledger(AccountName=particulars, TransctionType="Debit", Particulars=account_name, Amount=amount)
            l1.save()
        return render(request,'ledger.html',{"success":"Account Statement Added"})
    return render(request,'ledger.html')

def disp(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    list_accounts = ledger.objects.raw('SELECT DISTINCT AccountName,id from accounts_ledger')
    l=[]
    for i in list_accounts:
        if i.AccountName not in l:
            l.append(i.AccountName)
    if(request.method=="POST"):
        AccountName=request.POST['AccountName']
        Account = ledger.objects.all().filter(AccountName=AccountName)
        bal_debit = ledger.objects.filter(AccountName=AccountName,TransctionType="Debit").aggregate(debit=Sum('Amount'))
        bal_credit = ledger.objects.filter(AccountName=AccountName,TransctionType="Credit").aggregate(credit=Sum('Amount'))
        d=0
        c=0
        print(bal_debit)
        debit=bal_debit['debit']
        credit=bal_credit['credit']
        if credit==None:
            credit=0
        if debit==None:
            debit=0
        total = max(debit, credit)
        if debit>credit:
            d=debit-credit
            return render(request, 'dispLedger.html',
                          {'account': Account, 'list': l, 'debit': d,'total':total})
        else:
            c=credit-debit
            return render(request,'dispLedger.html',{'account':Account,'list':l,'credit':c,'total':total})
    else:
        return render(request,'dispLedger.html',{'list':l})


