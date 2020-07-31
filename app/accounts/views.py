from django.shortcuts import render,redirect
from .models import ledger,Payments,Receipts,Account
from django.db.models import Avg, Count, Min, Sum,Max
# Create your views here.
from addshg.models import Loan,shg
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
        l = ledger(AccountName=account_name,TransctionType=transctionType,Particulars=particulars,Amount=amount,RegIMO=request.user.username)
        l.save()
        if transctionType=="Debit":
            l1=ledger(AccountName=particulars,TransctionType="Credit",Particulars=account_name,Amount=amount,RegIMO=request.user.username)
            l1.save()
        else:
            l1 = ledger(AccountName=particulars, TransctionType="Debit", Particulars=account_name, Amount=amount,RegIMO=request.user.username)
            l1.save()
        return render(request,'ledger.html',{"success":"Account Statement Added"})
    return render(request,'ledger.html')

def disp(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    list_accounts = ledger.objects.raw('SELECT DISTINCT AccountName,id from accounts_ledger WHERE RegIMO=%s',[request.user.username])
    l=[]
    for i in list_accounts:
        if i.AccountName not in l:
            l.append(i.AccountName)
    if(request.method=="POST"):
        AccountName=request.POST['AccountName']
        Account = ledger.objects.all().filter(AccountName=AccountName,RegIMO=request.user.username)
        bal_debit = ledger.objects.filter(AccountName=AccountName,TransctionType="Debit",RegIMO=request.user.username).aggregate(debit=Sum('Amount'))
        bal_credit = ledger.objects.filter(AccountName=AccountName,TransctionType="Credit",RegIMO=request.user.username).aggregate(credit=Sum('Amount'))
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

def edit(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    edit_details=ledger.objects.filter(RegIMO=request.user.username,TransctionType="Debit")
    if request.method=="POST":
        if "edit-button" in request.POST:
            acc = request.POST["account"]
            ttype = request.POST["TransctionType"]
            part = request.POST["particulars"]
            amt = request.POST["amount"]
            l=ledger(AccountName=acc, TransctionType=ttype, Particulars=part, Amount=amt,RegIMO=request.user.username)
            l.save()
            if ttype=="Debit":
                l=ledger(AccountName=part, TransctionType="Credit", Particulars=acc, Amount=amt,RegIMO=request.user.username)
                l.save()
            else:
                l=ledger(AccountName=part, TransctionType="Debit", Particulars=acc, Amount=amt,RegIMO=request.user.username)
                l.save()
            return render(request,"edit.html",{"success":"Successfully Updated"})
        acc=request.POST["account"]
        ttype=request.POST["TransctionType"]
        part = request.POST["particulars"]
        amt = request.POST["amount"]
        edit_l = ledger.objects.filter(AccountName=acc, TransctionType=ttype, Particulars=part, Amount=amt,RegIMO=request.user.username).delete()
        if ttype == "Debit":
            edit_l = ledger.objects.filter(AccountName=part, TransctionType="Credit", Particulars=acc,
                                           Amount=amt,RegIMO=request.user.username).delete()
        else:
            edit_l = ledger.objects.filter(AccountName=part, TransctionType="Debit", Particulars=acc,
                                           Amount=amt,RegIMO=request.user.username).delete()
        if request.POST["action"]=="delete":
            return render(request,"edit.html",{"success":"Successfully Deleted"})
        return render(request, "dispedit.html", {"an": acc, "tt": ttype, "part": part, "amt": amt})
    return render(request, "edit.html", {"details": edit_details})

def receipts(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    if request.method=='POST':
        mem=request.POST['Memfees']
        fines=request.POST['Fines']
        rmkfunds=request.POST['Rmkfunds']
        prin=request.POST['Principal']
        intr=request.POST['Interests']
        openbal=request.POST['Openingbal']
        shgloans = request.POST['Shgloans']
        fees = request.POST['Feesandcharges']
        misc=request.POST['Misc']
        sal = request.POST['Salaries']
        adexp = request.POST['Adminexpenses']
        stat = request.POST['Stationery']
        mis = request.POST['Micellaneous']
        closingbal = request.POST['closingbal']
        p = Payments(Shgloans=shgloans, Closingbal=closingbal, Feesandcharges=fees, Salaries=sal, Adminexpenses=adexp,
                     Stationery=stat, Micellaneous=mis, RegIMO=request.user.username)
        p.save()
        r=Receipts(Memfees=mem,Fines=fines,Rmkfunds=rmkfunds,Principal=prin,Interests=intr,Openingbal=openbal,RegIMO=request.user.username,Micellaneous=misc)
        r.save()
        return render(request,"receipts.html",{"content":"Successfully Added"})
    else:
        amt=Loan.objects.filter(RegIMO=request.user.username).aggregate(princ=Sum('LoanRepayment'))
        intr=Loan.objects.filter(RegIMO=request.user.username).aggregate(interest=Sum('Interest'))
        ShgLoan=shg.objects.filter(Registration_id_imo=request.user.username).aggregate(shgl=Sum('Amount'))
        principal_amount=amt['princ']
        total_intr=intr['interest']
        amt=ShgLoan['shgl']
        return render(request,"receipts.html",{"principal":principal_amount,"interest":total_intr,"Amount":amt})


def RandPDisplay(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    total=Receipts.objects.filter(RegIMO=request.user.username).aggregate(ob=Max('Openingbal'),mf=Sum('Memfees'),fines=Sum('Fines'),rf=Sum('Rmkfunds'),ms=Sum('Micellaneous'))
    total_amt=Loan.objects.filter(RegIMO=request.user.username).aggregate(princ=Sum('LoanRepayment'),interest=Sum('Interest'))
    pay_total=Payments.objects.filter(RegIMO=request.user.username).aggregate(cb=Min('Closingbal'),shgl=Sum('Shgloans'),fac=Sum('Feesandcharges'),sal=Sum('Salaries'),ae=Sum('Adminexpenses'),sta=Sum('Stationery'),ms=Sum('Micellaneous'))
    total_loan=shg.objects.filter(Registration_id_imo=request.user.username).aggregate(shgl=Sum('Amount'))
    receipts_total=total['ob']+total['mf']+total['fines']+total['rf']+total['ms']+total_amt['princ']+total_amt['interest']
    payments_total=pay_total['cb']+pay_total['fac']+pay_total['sal']+pay_total['ae']+pay_total['sta']+pay_total['ms']+total_loan['shgl']
    if receipts_total>payments_total:
        ex=receipts_total-payments_total
        return render(request,"RPdisp.html",{"RP":total,"RPAmt":total_amt,"PT":pay_total,"loan":total_loan,"excess1":ex,"bal":receipts_total})
    else:
        ex=payments_total-receipts_total
        return render(request,"RPdisp.html",{"RP":total,"RPAmt":total_amt,"PT":pay_total,"loan":total_loan,"excess2":ex,"bal":payments_total})

def IandEDisplay(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    total_amt = Loan.objects.filter(RegIMO=request.user.username).aggregate(interest=Sum('Interest'))
    total = Receipts.objects.filter(RegIMO=request.user.username).aggregate(mf=Sum('Memfees'),fines=Sum('Fines'),ms=Sum('Micellaneous'))
    pay_total = Payments.objects.filter(RegIMO=request.user.username).aggregate(fac=Sum('Feesandcharges'),sal=Sum('Salaries'),ae=Sum('Adminexpenses'),ms=Sum('Micellaneous'))
    income_total=total_amt['interest']+total['fines']+total['mf']+total['ms']
    exp_total=pay_total['ae']+pay_total['sal']+pay_total['fac']+pay_total['ms']
    if income_total>exp_total:
        ex=income_total-exp_total
        return render(request,"IEdisp.html",{"RP":total,"RPAmt":total_amt,"PT":pay_total,"excess1":ex,"bal":income_total})
    else:
        ex = exp_total - income_total
        return render(request, "IEdisp.html", {"RP": total, "RPAmt": total_amt, "PT": pay_total, "excess2": ex,"bal":exp_total})

def BalanceSheet(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    total = Receipts.objects.filter(RegIMO=request.user.username).aggregate(ob=Max('Openingbal'), mf=Sum('Memfees'),
                                                                            fines=Sum('Fines'), rf=Sum('Rmkfunds'),
                                                                            ms=Sum('Micellaneous'))
    total_amt = Loan.objects.filter(RegIMO=request.user.username).aggregate(princ=Sum('LoanRepayment'),
                                                                            interest=Sum('Interest'))
    pay_total = Payments.objects.filter(RegIMO=request.user.username).aggregate(cb=Min('Closingbal'),
                                                                                shgl=Sum('Shgloans'),
                                                                                fac=Sum('Feesandcharges'),
                                                                                sal=Sum('Salaries'),
                                                                                ae=Sum('Adminexpenses'),
                                                                                sta=Sum('Stationery'),
                                                                                ms=Sum('Micellaneous'))
    total_loan = shg.objects.filter(Registration_id_imo=request.user.username).aggregate(shgl=Sum('Amount'))
    receipts_total = total['ob'] + total['mf'] + total['fines'] + total['rf'] + total['ms'] + total_amt['princ'] + \
                     total_amt['interest']
    payments_total = pay_total['cb'] + pay_total['fac'] + pay_total['sal'] + pay_total['ae'] + pay_total['sta'] + \
                     pay_total['ms'] + total_loan['shgl']
    income_total = total_amt['interest'] + total['fines'] + total['mf'] + total['ms']
    exp_total = pay_total['ae'] + pay_total['sal'] + pay_total['fac'] + pay_total['ms']
    ex1=0
    ex2=0
    c=0
    if receipts_total>payments_total:
        ex1=receipts_total-payments_total
    else:
        ex2=payments_total-receipts_total
    ex3=0
    ex4=0
    d=0
    if income_total>exp_total:
        ex3=income_total-exp_total
    else:
        ex4=exp_total-income_total
    cap=total_loan['shgl']+pay_total['sta']+pay_total['cb']
    assests=total_amt['princ']+total['ob']+total['rf']
    if ex1>ex2:
        cap=cap+ex1
        c=1
    else:
        assests=assests+ex2
    if ex4>ex3:
        d=1
        cap=cap+ex4
    else:
        assests=assests+ex3
    return render(request,"balsheet.html",{"loan":total_loan,"RP": total, "RPAmt": total_amt, "PT": pay_total,"cap_amt":cap,"assests_total":assests,"ex1":ex1,"ex2":ex2,"ex3":ex3,"ex4":ex4,"c":c,"d":d})

def FinRecords(request):
    return render(request,"financial_index.html")

def CashAccountDisp(request):
    AccountName = "Cash"
    Account = ledger.objects.all().filter(AccountName=AccountName, RegIMO=request.user.username)
    bal_debit = ledger.objects.filter(AccountName=AccountName, TransctionType="Debit",
                                      RegIMO=request.user.username).aggregate(debit=Sum('Amount'))
    bal_credit = ledger.objects.filter(AccountName=AccountName, TransctionType="Credit",
                                       RegIMO=request.user.username).aggregate(credit=Sum('Amount'))
    d = 0
    c = 0
    print(bal_debit)
    debit = bal_debit['debit']
    credit = bal_credit['credit']
    if credit == None:
        credit = 0
    if debit == None:
        debit = 0
    total = max(debit, credit)
    if debit > credit:
        d = debit - credit
        return render(request, 'dispLedger.html',
                      {'account': Account, 'debit': d, 'total': total})
    else:
        c = credit - debit
        return render(request, 'dispLedger.html', {'account': Account, 'credit': c, 'total': total})


def allAcc(request):
    if request.method=="POST":
        field=request.POST['field']
        RandP=request.POST['RandP']
        IandE=request.POST['IandE']
        balsheet=request.POST['balsheet']
        amount=request.POST['amount']
        acc = Account(Field=field,RandP=RandP,IandE=IandE,BalSheet=balsheet,Amount=amount)
        acc.save()
        return render(request,"generic.html")
    return render(request,"generic.html")

def RandPDisplay(request):
    rec=Account.objects.raw('SELECT Field,id from accounts_account WHERE RandP=%s',['Receipts'])
    pay=Account.objects.raw('SELECT Field,id from accounts_account WHERE RandP=%s',['Payments'])
    l1=[]
    l2=[]
    for i in rec:
        if i.Field not in l1:
            l1.append(i.Field)
    for j in pay:
        if j.Field not in l2:
            l2.append(j.Field)
    s=[]
    t=[]
    for i in range(len(l1)):
        s.append(0)
    for j in range(len(l2)):
        t.append(0)
    for i in range(len(l1)):
        s[i]=Account.objects.filter(RandP="Receipts",Field=l1[i]).aggregate(a=Sum("Amount"))
    for i in range(len(l2)):
        t[i]=Account.objects.filter(RandP="Payments",Field=l2[i]).aggregate(b=Sum("Amount"))
    rec_total=Account.objects.filter(RandP="Receipts").aggregate(rec_sum=Sum("Amount"))
    pay_total=Account.objects.filter(RandP="Payments").aggregate(pay_sum=Sum("Amount"))
    l3=[]
    for i in range(max(len(l1),len(l2))):
        dict={}
        if i<len(l1):
            dict['rec_field']=l1[i]
            dict['rec_amt']=s[i]['a']
        if i<len(l2):
            dict['pay_field']=l2[i]
            dict['pay_amt']=t[i]['b']
        l3.append(dict)
    if rec_total['rec_sum']>pay_total['pay_sum']:
        ex1=rec_total['rec_sum']-pay_total['pay_sum']
        print(ex1)
        return render(request,"RandPdisp.html",{"rp":l3,"rec_total":rec_total,"ex1":ex1})
    else:
        ex2=pay_total['pay_sum']-rec_total['rec_sum']
        return render(request, "RandPdisp.html",
                          {"rp": l3, "rec_total": pay_total['pay_sum'], "ex2": ex2})


def IandEDisplay(request):
    inc=Account.objects.raw('SELECT Field,id from accounts_account WHERE IandE=%s',['Income'])
    exp=Account.objects.raw('SELECT Field,id from accounts_account WHERE IandE=%s',['Exp'])
    l1=[]
    l2=[]
    for i in inc:
        if i.Field not in l1:
            l1.append(i.Field)
    for j in exp:
        if j.Field not in l2:
            l2.append(j.Field)
    print(l2)
    s=[]
    t=[]
    for i in range(len(l1)):
        s.append(0)
    for j in range(len(l2)):
        t.append(0)
    for i in range(len(l1)):
        s[i]=Account.objects.filter(IandE="Income",Field=l1[i]).aggregate(a=Sum("Amount"))
    for i in range(len(l2)):
        t[i]=Account.objects.filter(IandE="Exp",Field=l2[i]).aggregate(b=Sum("Amount"))
    inc_total=Account.objects.filter(IandE="Income").aggregate(rec_sum=Sum("Amount"))
    print(inc_total['rec_sum'])
    exp_total=Account.objects.filter(IandE="Exp").aggregate(pay_sum=Sum("Amount"))
    print(exp_total['pay_sum'])
    print(t)
    l3=[]
    for i in range(max(len(l1),len(l2))):
        dict={}
        if i<len(l1):
            dict['inc_field']=l1[i]
            dict['inc_amt']=s[i]['a']
        if i<len(l2):
            dict['exp_field']=l2[i]
            dict['exp_amt']=t[i]['b']
        l3.append(dict)
    if inc_total['rec_sum']>exp_total['pay_sum']:
        ex1=inc_total['rec_sum']-exp_total['pay_sum']
        return render(request,"IandEdisp.html",{"rp":l3,"rec_total":inc_total,"ex1":ex1})
    else:
        ex2=exp_total['pay_sum']-inc_total['rec_sum']
        return render(request, "Iandedisp.html",
                          {"rp": l3, "rec_total": exp_total['pay_sum'], "ex2": ex2})

def BalSheetDisp(request):
    asset = Account.objects.raw('SELECT Field,id from accounts_account WHERE BalSheet=%s', ['Assets'])
    lia = Account.objects.raw('SELECT Field,id from accounts_account WHERE BalSheet=%s', ['Lia'])
    l1 = []
    l2 = []
    for i in asset:
        if i.Field not in l1:
            l1.append(i.Field)
    for j in lia:
        if j.Field not in l2:
            l2.append(j.Field)
    print(l2)
    s = []
    t = []
    for i in range(len(l1)):
        s.append(0)
    for j in range(len(l2)):
        t.append(0)
    for i in range(len(l1)):
        s[i] = Account.objects.filter(BalSheet="Assets", Field=l1[i]).aggregate(a=Sum("Amount"))
    for i in range(len(l2)):
        t[i] = Account.objects.filter(BalSheet="Lia", Field=l2[i]).aggregate(b=Sum("Amount"))
    as_total = Account.objects.filter(BalSheet="Assets").aggregate(rec_sum=Sum("Amount"))
    lia_total = Account.objects.filter(BalSheet="Lia").aggregate(pay_sum=Sum("Amount"))
    l3 = []
    for i in range(max(len(l1), len(l2))):
        dict = {}
        if i < len(l1):
            dict['as_field'] = l1[i]
            dict['as_amt'] = s[i]['a']
        if i < len(l2):
            dict['lia_field'] = l2[i]
            dict['lia_amt'] = t[i]['b']
        l3.append(dict)
    inc_total = Account.objects.filter(IandE="Income").aggregate(rec_sum=Sum("Amount"))
    exp_total = Account.objects.filter(IandE="Exp").aggregate(pay_sum=Sum("Amount"))
    rec_total = Account.objects.filter(RandP="Receipts").aggregate(rec_sum=Sum("Amount"))
    pay_total = Account.objects.filter(RandP="Payments").aggregate(pay_sum=Sum("Amount"))
    c=0
    d=0
    if inc_total['rec_sum']>exp_total['pay_sum']:
        c=1
        ex1=inc_total['rec_sum']-exp_total['pay_sum']
        as_total['rec_sum']=as_total['rec_sum']+ex1
    else:
        ex1=exp_total['pay_sum']-inc_total['rec_sum']
        lia_total['pay_sum']=lia_total['pay_sum']+ex1
    if rec_total['rec_sum']>pay_total['pay_sum']:
        ex3=rec_total['rec_sum']-pay_total['pay_sum']
        lia_total['pay_sum']=lia_total['pay_sum']+ex3
    else:
        d=1
        ex3=pay_total['pay_sum']-rec_total['rec_sum']
        as_total['rec_sum']=as_total['rec_sum']+ex3
    return render(request,"bals.html",{"sheet":l3,"ie":ex1,"rp":ex3,"c":c,"d":d,"as_total":as_total,"lia_total":lia_total})