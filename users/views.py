from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import LoginForm, RegisterForm
from .models import User


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            messages.warning(request, "invalid form input")
            return redirect("index")

        data = form.cleaned_data
        user = authenticate(username=data["email"], password=data["password"])

        if not user:
            messages.warning(request, "Invalid Credentials")
            return redirect("login")

        login(request, user)
        return redirect("index")
    return render(request, "users/login.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if not form.is_valid():
            print(form.errors)
            messages.warning(request, "invalid form input")
            return redirect("register")
        data = form.cleaned_data
        try:
            user = User.objects.get(email=data["email"])
            messages.warning(request, "Account already exists with this email address")
        except User.DoesNotExist:
            user = User(
                email=data["email"],
                full_name=data["full_name"],
                is_doctor=data["is_doctor"],
            )
            user.set_password(data["password"])
            user.save()

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "users/register.html")


def logout_view(request):
    logout(request)
    return redirect("index")