from django.shortcuts import render,reverse,HttpResponseRedirect,get_object_or_404
from .forms import RegisterForm,LoginForm,UserProfileUpdateForm,UserPasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.decorators import anonymous_required
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

@anonymous_required
def register(request):
    form=RegisterForm(data=request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        username=form.cleaned_data.get('username')
        sex=form.cleaned_data.get('sex')
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user,sex=sex)
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())
    return render(request,'auth/register.html',context={'form':form})

@anonymous_required
def userlogin(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        password=form.cleaned_data.get('password')
        username=form.cleaned_data.get('username')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())

    return render(request,'auth/login.html',context={'form':form})

def userlogout(request):
    username=request.user.username
    logout(request)
    return HttpResponseRedirect(reverse('userlogin'))

def userprofile(request,username):
    user=get_object_or_404(User,username=username)
    return render(request,'auth/userprofile.html',context={'user':user,'page':'profile'})

def user_settings(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    initial = {'sex': sex, 'bio': bio, 'profile_photo': profile_photo}
    form=UserProfileUpdateForm(initial=initial,instance=request.user,data=request.POST or None,files=request.FILES or None)

    if form.is_valid():
        user = form.save(commit=True)
        bio = form.cleaned_data.get('bio', None)
        sex = form.cleaned_data.get('sex', None)
        profile_photo = form.cleaned_data.get('profile_photo', None)
        user.userprofile.sex = sex
        user.userprofile.profile_photo = profile_photo
        user.userprofile.bio = bio
        user.userprofile.save()
        return HttpResponseRedirect(reverse('userprofile', kwargs={'username': user.username}))
    return render(request, 'auth/user_setings.html', context={'form': form,'page':'settings'})

def user_about(request,username):
    user=get_object_or_404(User,username=username)
    return render(request, 'auth/about.html', context={'user': user,'page':'about'})

def user_password_change(request):
    form = UserPasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        update_session_auth_hash(request, user)
        return HttpResponseRedirect(reverse('userprofile', kwargs={'username': request.user.username}))
    return render(request,'auth/password_change.html',context={'form':form,'page':'passchange'})

