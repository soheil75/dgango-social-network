from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in seccessfully','success')
                return redirect('posts:all_posts')
            else:
                messages.error(request,'wrong username or password','danger')
    else:
        form = UserLoginForm()
    return render(request,'account/login.html',{'form':form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],cd['email'],cd['password'])
            login(request,user)
            messages.success(request,'you registerd successfully','success')
            return redirect('posts:all_posts')
    else:
        form = UserRegisterForm()
    return render(request,'account/register.html',{'form':form})

def user_logout(request):
    logout(request)
    messages.success(request,'you loged out successfully','success')
    return redirect('posts:all_posts')