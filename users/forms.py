from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template.context_processors import request
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class RegisterForm(forms.ModelForm):
    password=forms.CharField(required=True,label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confrim=forms.CharField(required=True,label='Password confrim',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex=forms.ChoiceField(required=True,choices=UserProfile.SEX)
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email','sex','password','password_confrim']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields ['first_name'].required=True
        self.fields ['last_name'].required=True
        self.fields ['username'].help_text=False



    def clean(self):
        password=self.cleaned_data.get('password')
        password_confrim=self.cleaned_data.get('password_confrim')
        if password !=password_confrim:
            self.add_error('password','parolalar eşleşmedi')
            self.add_error('password_confrim', 'parolalar eşleşmedi')

    def clean_email(self):
        email=self.cleaned_data.get('email')
        email=email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("bu email sistemde kayıtlı")
        return email


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("bu kullanıcı adı sistemde mevcut")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, max_length=50, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        if not user:
            raise forms.ValidationError("hatalı kullanıcı adı veya şifre girdiniz")





class UserProfileUpdateForm(forms.ModelForm):
    sex = forms.ChoiceField(required=True, choices=UserProfile.SEX)
    profile_photo = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email','sex', 'profile_photo', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['bio'].widget.attrs['rows'] = 5

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        # eğer hiç email adresi girilmemişse
        if not email:
            raise forms.ValidationError('Lütfen Email Bilgisi Giriniz')

        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('Bu email adresi sistemde mevcut.')

        return email

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
