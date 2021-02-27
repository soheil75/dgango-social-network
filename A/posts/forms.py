from django import forms
from django.db import models
from django.db.models import fields
from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)