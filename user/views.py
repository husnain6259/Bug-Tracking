from django.shortcuts import render
from django.db.models import Q
from user.forms import SignUpForm,LoginForm
from user.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest


def joinUs(request):
    return render(request, 'base/home.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # breakpoint()
            user.role = request.POST.get('role') 
            user.save()
            return redirect("login")

        return render(request, "base/signup.html", {"form": form, "role": request.POST.get('role')})
    else:
        role = request.GET.get('role')
        if role not in ['manager', 'developer', 'qa']:
            return HttpResponseBadRequest("Invalid role!")
        form = SignUpForm()
        return render(request, "base/signup.html", {"form": form, "role": role})


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, "Login Successfully")
                return redirect('index')  # All roles redirect to index
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'base/login.html', {'form': form, 'msg': msg})


def logoutView(request):
    logout(request)
    return redirect('login')
