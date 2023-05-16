from django.urls import path
from . import views

app_name = "consultants"
urlpatterns = [
    path("", views.home, name="home"),
    path("favicon.ico", views.favicon),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("login/forgotpassword/", views.forgot_password, name="forgot_password"),
    path("login/resetpassword/<str:token>", views.reset_password, name="reset_password"),
    path("sendcase/", views.sendcase, name="sendcase"),
    path("mycases/", views.mycases, name="mycases"),
    path("addcertification/", views.addcertification, name="addcertification"),
    path("mycertifications/", views.mycertifications, name="mycertifications")
]