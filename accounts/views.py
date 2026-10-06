from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        Profile.objects.create(user=user)

        login(request, user)

        return redirect("home")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request):
    profile = request.user.profile

    subscription = (
        request.user.subscriptions
        .filter(status="active")
        .select_related("plan")
        .first()
    )

    payments = (
        request.user.payments
        .select_related("subscription", "subscription__plan")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "subscription": subscription,
            "payments": payments,
        },
    )
