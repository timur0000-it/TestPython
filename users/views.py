# GLOBAL
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
# LOCAL
from .models import AbstractUser,Seller,CustomerUser
from .forms import SignUpForm,SignInForm
import random
# Create your views here.

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            number2=''
            for i in range(4):
                number2+=str(random.randint(0,9))
            user.parol = number2
            user.save()
            gmail(user)
            login(request,user)
            return redirect('shop:all_products')
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username','').strip()
            password = form.cleaned_data.get('password','').strip()
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('shop:all_products')
            else:
                print(user)
                error_message = 'Неверный логин или пороль'
                return render(request,'signin.html',{'form':form,'error_message':error_message})
    else:
        form = SignInForm()
    return render(request,'signin.html',{'form':form})

def signout(request):
    logout(request)
    return redirect('users:signin')    

def gmail(user):
    subject = 'Поздравляем с регистрацией'
    message = f'Привет , {user.username}! рады приветствовать на нашем сайте код {user.parol} http://127.0.0.1:8000/users/kod/{user.username}'
    to_email = user.email
    send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[to_email]
            )
    
def kod(request,username):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomerUser.objects.get(username=username)
        if code == user.parol:
            user.is_active=True
            user.save()
            login(request,user)
            return redirect('shop:all_products')
    return render(request,'parol.html')
    # user.is_active = True
    # user.save()