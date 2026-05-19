from django import forms

from .models import AbstractUser,Seller,CustomerUser
from django.core.exceptions import ValidationError
# class SignUpForm(forms.Form):
#     username = forms.CharField(max_length=100, required=True,label='Имя пользователя',widget=forms.TextInput(attrs={'class':'username'}))
#     email = forms.EmailField(required=True,label='Почта')
#     photo = forms.ImageField(required=False)
#     phone_number = forms.CharField(max_length=20,required=True)
#     role = forms.ChoiceField(choices=CustomerUser.USER_ROLES)
#     password = forms.CharField(required=True,max_length=150)
    
class SignUpForm(forms.ModelForm):
    password_1=forms.CharField(required=True,label='Пароль')
    password_2=forms.CharField(required=True,label='Повторить пароль')
    class Meta:
        model = CustomerUser
        fields = ('username','email','photo','role','phone_number','password_1','password_2')
        
    def clean(self):
        cleaned = super().clean()
        password_1= self.cleaned_data.get('password_1')
        password_2= self.cleaned_data.get('password_2')
        if password_1 != password_2:
            raise ValidationError('Пароли не совпадают')
        return cleaned
        
    def save(self):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password_1')
        user.set_password(password) 
        user.save()
        if user.is_seller:
            Seller.objects.create(user=user)
        return user
       
class SignInForm(forms.Form):
    username = forms.CharField(max_length=150,required=True,label='Имя пользователя')
    password = forms.CharField(required=True,max_length=150,label='Пароль')

class ActivationCodeForms(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly':'readonly'}),required=False)
    code = forms.CharField(max_length=4,min_length=4,label='Код (4 цифры)')