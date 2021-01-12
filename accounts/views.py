from django.contrib.auth import login, logout
from django.http.response import HttpResponseRedirect
from accounts.forms import UserCreationForm, UserLoginForm
from django.shortcuts import render



def register_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_object = form.cleaned_data.get('user_object')
        login(request, user_object)
        return HttpResponseRedirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')