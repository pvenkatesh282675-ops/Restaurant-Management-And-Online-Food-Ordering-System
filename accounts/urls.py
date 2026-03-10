from django.urls import path
from accounts.views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("resend-otp/", resend_otp, name="resend_otp"),
    path("forget-password/", forget_password, name="forget_password"),
    path("verify-reset-otp/",verify_reset_otp, name="verify_reset_otp"),
    path("reset-password/", reset_password, name="reset_password"),
]