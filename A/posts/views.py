from django.shortcuts import redirect, render,get_object_or_404
from .models import Post
from .forms import AddPostForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

# Create your views here.

def  all_posts(request):
    posts = Post.objects.all()
    return render(request,'posts/all_posts.html',{'posts':posts})

def post_detail(request, year, month, day, slug):
    #برای تطابق زمان های گرفته شده با زمان موجود در دیتابیس از لوک اپ ها استفاده شده
    post = get_object_or_404(Post,created__year=year, created__month=month, created__day=day, slug=slug)
    return render(request,'posts/post_detail.html',{'post':post})

@login_required
def add_post(request,user_id):
    if request.user.id == 'POST':
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request,'post saved','success')
                return redirect('account:dashboard',user_id)
        else:
            form = AddPostForm()
        return render(request,'posts/add_post.html',{'form':form})
    else:
        return redirect(request,'posts:all_posts')

@login_required
def post_delete(request,user_id,post_id):
    if user_id == request.user.id:
        Post.objects.filter(pk=post_id).delete()
        messages.success(request,'post deleted successfully','success')
        return redirect('account:dashboard',user_id)
    else:
        return redirect('posts:all_posts')