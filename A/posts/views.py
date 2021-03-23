from django import forms
from django.http import request
from django.shortcuts import redirect, render,get_object_or_404
from .models import Post ,Comment
from .forms import AddPostForm,EditPostForm,AddCommentForm,AddReplyForm
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
    comments = Comment.objects.filter(post=post,is_reply=False)
    reply_form = AddReplyForm()
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request,'Your comment submited')
    else:
        form = AddCommentForm()
    return render(request,'posts/post_detail.html',{'post':post,'comments':comments,'form':form,'reply':reply_form})

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

@login_required
def post_edit(request,user_id,post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post,pk=post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST,instance=post)
            if form.is_valid:
                ep = form.save(commit=False)
                ep.slug = slugify(form.cleaned_data['body'][:30])
                ep.save()
                messages.success(request,'your post edited successfully','success')
                return redirect('account:dashboard',user_id)
        else:
            form = EditPostForm(instance=post)
            return render(request,'posts/edit_post.html',{'form':form})
    else:
        return redirect('posts:all_posts')

@login_required
def add_reply(request,post_id,comment_id):
    post = get_object_or_404(Post,id=post_id)
    comment = get_object_or_404(Comment,pk=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request,'you send a reply','success')
    return redirect('posts:post_detail',post.created.year,post.created.month,post.created.day,post.slug)
