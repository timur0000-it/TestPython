# GLOBAL
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
# LOCAL
from .models import AbstractUser,Seller,CustomerUser,ActivationCode
from .forms import SignUpForm,SignInForm,ActivationCodeForms
import random
# Create your views here.
def login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        return redirect('users:signin')
    return wrapper

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            request.session['active_email'] = user.email
            return redirect('users:verify_code')
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
                return redirect('users:get_all_users')
            else:
                print(user)
                error_message = 'Неверный логин или пороль'
                return render(request,'signin.html',{'form':form,'error_message':error_message})
    else:
        form = SignInForm()
    return render(request,'signin.html',{'form':form})
@login_required
def signout(request):
    logout(request)
    return redirect('users:signin')    


@login_required
def get_all_users(request):
    all_users = CustomerUser.objects.all()
    return render(request,'get_all_users.html',{'all_users':all_users})
    
def verify_code(request):
    if request.method == 'POST':
        form = ActivationCodeForms(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code','')
            email = request.session['active_email']
            user1 = CustomerUser.objects.filter(email=email).first()
            user_code = ActivationCode.objects.filter(user=user1).first()
            if not user_code:
                user1.delete()
                messages.warning(request, 'Вы не подтвердили код пожайлуста зарегестрируйтесь заново')
                return redirect('users:signin')  
            activation = user_code.check_code(code)
            if activation[0] == True:
                user1.is_active=True
                user1.save()
                login(request,user1)
                messages.success(request, 'Поздравляем с регистрацией')
                return redirect('shop:all_products')
            else:
                form = ActivationCodeForms()
                email = request.session['active_email']
                form.fields['email'].initial=email
                error=activation[1]
                return render(request,'verify_code.html',{'form':form,'error':error})
    else:
        form = ActivationCodeForms()
        email = request.session['active_email']
        form.fields['email'].initial=email
    return render(request,'verify_code.html',{'form':form})



