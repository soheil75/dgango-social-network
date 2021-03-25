from django.shortcuts import redirect, render,get_object_or_404
from .forms import UserLoginForm,UserRegisterForm,EditProfileForm,PhoneLoginFrom,VerifyCodeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from posts.models import Post
from .models import Profile,Relaiton
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from django.http import JsonResponse



def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in seccessfully','success')
                if next:
                    return redirect(next)
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

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'you loged out successfully','success')
    return redirect('posts:all_posts')

@login_required
def user_dashboard(request,user_id):
    user = get_object_or_404(User,id = user_id)
    posts = Post.objects.filter(user=user)
    is_following = False
    relation = Relaiton.objects.filter(from_user=request.user,to_user=user)
    if relation.exists():
        is_following = True
    #اینجا چک کردیم ایا رابطه ای بین من بیننده پروفایل با صاحب پروفایل وجود دارد یا نه
    self_dash = False
    if request.user.id == user_id:
        self_dash = True
    return render(request,'account/dashboard.html',{'user':user,'posts':posts,'self_dash':self_dash,'is_following':is_following})

@login_required
def edit_profile(request,user_id):
    user = get_object_or_404(User,pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request,'your profile edited','success')
            return redirect('account:dashboard',user_id)
    else:
        form = EditProfileForm(instance=user.profile,initial={'email':request.user.email})
    return render(request,'account/edit_profile.html',{'form':form})

def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginFrom(request.POST)
        if form.is_valid():
            #خود جنگو صفر اول عدد وارد شده رو حذف میکند و ما در اینجا دوباره اضافش کردیم
            phone = f"0{form.cleaned_data['phone']}"
            rand_num = randint(1000,9999)
            #Kavenegar API
            api = KavenegarAPI('4E50376B5A745152496B50503749416D445A4E4771686B794C59414F6C784163746436366C4663593874383D')
            params = { 'sender' : '', 'receptor': phone, 'message' :rand_num }
            api.sms_send(params)
            return redirect('account:verify',phone,rand_num)
    else:
        form = PhoneLoginFrom()
    return render(request,'account/phone_login.html',{'form':form})

def verify(request,phone,rand_num):
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            verify_code = form.cleaned_data['code']
            if verify_code == rand_num:
                profile = get_object_or_404(Profile,phone=phone)
                user = get_object_or_404(User,profile__id=profile.id)
                #profile__id یک فیلد از User است
                #Profile و User توسط یک رابطه به هم وصل هستن پس از طریق اینیکی میتوان به اونیکی رسید
                login(request,user)
                messages.success(request,'log in','success')
                return redirect('posts:all_posts')
            else:
                messages.error(request,'your code is wrong','danger')
    else:
        form = VerifyCodeForm()
    return render(request,'account/verify.html',{'form':form})

@login_required
def follow(request):
    if request.method =='POST':
        user_id = request.POST['user-id']
        following = get_object_or_404(User,pk=user_id)
        check_relation = Relaiton.objects.filter(from_user=request.user,to_user=following)
        if check_relation.exists():
            return JsonResponse({'status':'exists'})
        else:
            Relaiton(from_user=request.user,to_user=following).save()
            return JsonResponse({'status':'ok'})
        #چک کردیم اگر رابطه وجود داشت که هیچی و بعد باسخ دادیم به درخواست وگرنه یک رابطه ساختیم و بعد جواب دادیم

@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user-id']
        following = get_object_or_404(User,pk=user_id)
        check_relation = Relaiton.objects.filter(from_user=request.user,to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'notexist'})



