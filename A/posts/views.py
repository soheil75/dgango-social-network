from django.shortcuts import render,get_object_or_404
from .models import Post
# Create your views here.

def  all_posts(request):
    posts = Post.objects.all()
    return render(request,'posts/all_posts.html',{'posts':posts})

def post_detail(request, year, month, day, slug):
    #برای تطابق زمان های گرفته شده با زمان موجود در دیتابیس از لوک اپ ها استفاده شده
    post = get_object_or_404(Post,created_year=year, created_month=month, created_day=day, slug=slug)
    return render(request,'posts/post_detail.html',{'post':post})