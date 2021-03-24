from django import forms
from django.db.models import fields
from .models import Profile

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

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age','bio',)
        widgets = {
            # 'age':forms.Textarea(attrs={'class':'form-control','rows': 2}),
            'bio':forms.Textarea(attrs={'class':'form-control','rows': 2}),
        }

class PhoneLoginFrom(forms.Form):
    phone = forms.IntegerField()
    #یا فانکشن برای تست وجود داشتن یا نداشتن شماره موبایل کاربر درون دیتابیس هستش
    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
        #حتما باید از filter استفاده شود
        #چون get متد exists رو نداره و در صورت استفاده ارور میده
        if not phone.exists():
            raise forms.ValidationError('this phone nuber does not exists')
        #حتما باید self.cleaned_data['phone'] ریترن شود
        return self.cleaned_data['phone']

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()