from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from account.forms import LoginForm, RegisterForm, ProfileForm
from account.models import Profile


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, 'You are logged in successfully')
        return redirect('home')
    messages.error(request, 'Invalid username or password')
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out successfully')
    return redirect('home')


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully')
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('home')
    messages.error(request, 'Invalid username or password')
    return render(request, 'account/register.html', {'form': form})


def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                cd = form.cleaned_data
                profile.city = cd['city']
                profile.language = cd['language']
                profile.notify = cd['notify']
                profile.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('account:profile')
        else:
            form = ProfileForm(initial={'city': profile.city, 'language': profile.language, 'notify': profile.notify})
        return render(request, 'account/profile.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to access this page')
        return redirect('account:login')
