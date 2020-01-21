from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from login.models import AdminPassword, loginModel
import datetime

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        

        adminpassword = request.POST['admin_password']
        admin = AdminPassword.objects.all()

        flag = False

        for each in admin:
            if adminpassword == each.admin_password:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                auth.login(request, user)
                return redirect('stocks')
            else:
                flag = True

        if flag is True:
            return redirect('login')
        

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            user.save()
            loginmodel = loginModel(username=username, password=password, time=str(datetime.datetime.now()))
            loginmodel.save()
            auth.login(request, user)
            return redirect('stocks')
        else:
            return redirect('signin')


    return render(request, 'signin.html')


def login(request):
    auth.logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            user.save()
            loginmodel = loginModel(username=username, password=password, time=str(datetime.datetime.now()))
            loginmodel.save()
            auth.login(request, user)
            return redirect('stocks')
        else:
            return redirect('signin')


    return render(request, 'signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


def pagelock(request):
    return redirect('login')