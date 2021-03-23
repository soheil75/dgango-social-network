from django import forms

messages = {
    'required':'.پر کردن این فیلد اجباری است',
    'invalid':'.این فیلد باید با محتوای معتبر پر شود'
}

class UserLoginForm(forms.Form):
    username = forms.CharField(error_messages=messages,help_text='max 30 character', max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password = forms.CharField(error_messages=messages,help_text='max 40 character', max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(error_messages=messages, max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    email = forms.EmailField(error_messages=messages, max_length=50,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    password = forms.CharField(error_messages=messages, max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))