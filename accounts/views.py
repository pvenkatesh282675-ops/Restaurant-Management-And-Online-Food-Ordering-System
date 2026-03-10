from django.shortcuts import render , redirect

# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
from accounts.models import EmailOTP

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.create(user=user, otp=otp)

        send_mail(
            subject="Verify your e-DineIn account",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=f"<h2>Your OTP is {otp}</h2>"
        )

        request.session["user_id"] = user.id
        return redirect("verify_otp")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("home")
            messages.error(request, "Please verify your email first")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def verify_otp(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect("register")

    otp_obj = EmailOTP.objects.filter(user_id=user_id).first()
    if not otp_obj:
        messages.error(request, "OTP not found.")
        return redirect("register")

    if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
        otp_obj.delete()
        messages.error(request, "OTP expired. Please resend OTP.")
        return redirect("resend_otp")

    if request.method == "POST":
        if request.POST.get("otp") == otp_obj.otp:
            user = otp_obj.user
            user.is_active = True
            user.save()
            otp_obj.delete()
            messages.success(request, "Account verified. Please login.")
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_otp.html")


def resend_otp(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()

    if not user:
        return redirect("register")

    EmailOTP.objects.filter(user=user).delete()

    otp = str(random.randint(100000, 999999))
    EmailOTP.objects.create(user=user, otp=otp)

    send_mail(
        subject="Your new OTP",
        message=f"Your OTP is {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        html_message=f"<h2>Your new OTP is {otp}</h2>"
    )

    messages.success(request, "New OTP sent to your email")
    return redirect("verify_otp")

# FORGET PASSWORD - SEND OTP

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No account found with this email")
            return redirect("forget_password")

        # Delete old OTP if exists
        EmailOTP.objects.filter(user=user).delete()

        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.create(user=user, otp=otp)

        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=f"<h2>Your Password Reset OTP is {otp}</h2>"
        )

        request.session["reset_user_id"] = user.id
        messages.success(request, "OTP sent to your email")
        return redirect("verify_reset_otp")

    return render(request, "forget_password.html")

def verify_reset_otp(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        messages.error(request, "Session expired")
        return redirect("forget_password")

    otp_obj = EmailOTP.objects.filter(user_id=user_id).first()

    if not otp_obj:
        messages.error(request, "OTP not found")
        return redirect("forget_password")

    # OTP Expiry (5 minutes)
    if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
        otp_obj.delete()
        messages.error(request, "OTP expired")
        return redirect("forget_password")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if entered_otp == otp_obj.otp:
            otp_obj.delete()
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_reset_otp.html")


def reset_password(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forget_password")

    user = User.objects.filter(id=user_id).first()

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("reset_password")

        user.set_password(password)
        user.save()

        del request.session["reset_user_id"]

        messages.success(request, "Password reset successful. Please login.")
        return redirect("login")

    return render(request, "reset_password.html")