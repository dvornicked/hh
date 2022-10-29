from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from account.forms import LoginForm


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
