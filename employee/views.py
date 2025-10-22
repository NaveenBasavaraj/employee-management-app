from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


def home(request):
    return render(request, "employee/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a blank profile for the new user
            Profile.objects.get_or_create(user=user, defaults={"designation": "", "salary": 0})
            auth_login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("profile")
    else:
        form = UserCreationForm()
    return render(request, "employee/register.html", {"form": form})


@login_required
def profile(request):
    profile = getattr(request.user, "profile", None)
    return render(request, "employee/profile.html", {"profile": profile})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.designation = request.POST.get("designation", profile.designation)
        salary_val = request.POST.get("salary", "")
        try:
            if salary_val != "":
                profile.salary = int(salary_val)
        except ValueError:
            messages.error(request, "Salary must be a number.")
            return render(request, "employee/profile_edit.html", {"profile": profile})
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    return render(request, "employee/profile_edit.html", {"profile": profile})
