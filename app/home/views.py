from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout,login
from home.models import register

# Create your views here.
def index(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username=request.POST['nmo']
        password=request.POST['your_pass']
        print(username,password)
        user=authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('http://127.0.0.1:8000/portal')
        else:
            return render(request, 'login.html',{"msg":"Enter Correct Credentials"})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/login')

def reg(request):
    if request.method == 'POST' :
        nmo=request.POST['nmo']
        headname=request.POST['headname']
        address=request.POST['address']
        state=request.POST['state']
        phno=request.POST['phno']
        uniqueid=request.POST['uniqueid']
        password=request.POST['password']
        s=register(nmo=nmo,headname=headname,address=address,state=state,phno=phno,uniqueid=uniqueid,password=password)
        s.save()
        return render(request,'imo_portal.html')
    return render(request,'register.html')

def portal(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/login')
    return render(request,'imo_portal.html')