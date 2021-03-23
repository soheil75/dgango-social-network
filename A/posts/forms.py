from django import forms
from django.db import models
from django.db.models import fields
from .models import Post, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','rows': 2})
        }
        labels = {
            'body': ('body'),
        }
        help_texts = {
            'body': ('Some useful help text.'),
        }
        error_messages = {
            'body': {
                'max_length': ("This text is too long."),
            },
        }

class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','rows': 2})
        }
