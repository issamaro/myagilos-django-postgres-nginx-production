from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from .forms import AddCertificationForm, CasesForm, ForgotPasswordForm, ResetPasswordForm
from .models import Cases, Consultants, ForgotPassword, User
from .emailz import *
import hashlib
import secrets

# ----------GLOBAL TEMPLATES----------
LOGIN_TEMPLATE = "consultants/logs/login.html"
FORGOT_PASSWORD_TEMPLATE = "consultants/logs/forgot_password.html"
RESET_PASSWORD_TEMPLATE = "consultants/logs/reset_password.html"
RESET_EMAIL_TXT = "consultants/templates_files/reset_email.txt"
RESET_CONFIRMATION_EMAIL_TXT = "consultants/templates_files/reset_email_confirm.txt"

HOME_TEMPLATE = "consultants/mains/home.html"
SENDCASE_TEMPLATE = "consultants/mains/sendcase.html"
MYCASES_TEMPLATE = "consultants/mains/mycases.html"
ADDCERTIFICATION_TEMPLATE = "consultants/mains/addcertification.html"
MYCERTIFICATIONS_TEMPLATE = "consultants/mains/mycertifications.html"


# ----------FAVICON----------
@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request):
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 699.99 699.98">'
            + '<defs><style>.b{fill:#3756f5;}.c{fill:#2ce3a0;}</style></defs>'
            + '<path class="b" d="M350,97.17c-139.64,0-252.83,113.2-252.83,252.82s113.2,'
            + '252.82,252.83,252.82,252.82-113.2,252.82-252.82-113.2-252.82-252.82-252.82m0,'
            + '94.52c87.28,0,158.3,71.02,158.3,158.3s-71.02,158.3-158.3, '
            + '158.3-158.3-71.02-158.3-158.3,71.02-158.3,158.3-158.3"/>'
            + '<path class="c" d="M350,288.96c33.51,0,61.03,27.53,61.03,'
            + '61.03s-27.52,61.04-61.03,61.04-61.04-27.52-61.04-61.04,27.52-61.03,61.04-61.03"/>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )


# ----------LOGIN/LOGOUT/PASSWORD/ETC.----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("consultants:home")
    elif request.method == "GET":
        return render(request, LOGIN_TEMPLATE)
    elif request.method == "POST":
        user = {
            "username": request.POST["username"],
            "password": request.POST["password"]
        }
        user_auth = authenticate(request, **user)
        if user_auth is not None:
            login(request, user_auth)
            return redirect("consultants:home")
        else:
            return render(request, LOGIN_TEMPLATE, {
                "message": "Wrong credentials.",
                "helper_username": "Username: \"[firstname].[lastname]\""
            })


@login_required
def logout_view(request):
    logout(request)
    return render(request, LOGIN_TEMPLATE, {
        "logout": "Goodbye!"
    })


def forgot_password(request):
    if request.method == "GET":
        form = ForgotPasswordForm()
        return render(request, FORGOT_PASSWORD_TEMPLATE, {
            "form": form
        })
    elif request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                return render(request, FORGOT_PASSWORD_TEMPLATE, {
                    "form": form,
                    "message": "could not find a user with these credentials."
                })
            else:
                # ENCRYPTION
                salt = secrets.token_hex(16)
                secret_token = secrets.token_urlsafe(64)
                hashed_token = hashlib.pbkdf2_hmac('sha256', secret_token.encode('utf-8'), salt.encode('utf-8'), 100000)
                # FORGOT_CASE CREATION
                ForgotPassword.objects.create(
                    username=username,
                    email=email,
                    salt_and_hash=(salt + ":" + hashed_token.hex()),
                    active=True)
                # EMAIL WITH SECRET TOKEN
                reset_url = request.build_absolute_uri(
                    reverse("consultants:reset_password", args=[secret_token]))
                with open(RESET_EMAIL_TXT, "r") as emailf:
                    body = f"{emailf.read()}".format(
                        first_name=user.first_name, reset_url=reset_url)
                sendemail(
                    sender="aca@agilos.com",
                    password="Agilos123",
                    receiver=email,
                    subject=f"{user.first_name}, reset your password",
                    body=body
                )
                return HttpResponse(f"Email sent to {email}.")
        else:
            return render(request, FORGOT_PASSWORD_TEMPLATE, {
                "form": form
            })


def reset_password(request, token):
    if request.method == "GET":
        form = ResetPasswordForm()
        return render(request, RESET_PASSWORD_TEMPLATE, {
            "form": form,
            "token": token
        })
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            current_time = timezone.now()
            try:
                forgot_case = ForgotPassword.objects.get(username=username, active=True, expires_at__gt=current_time)
            except ForgotPassword.DoesNotExist:
                return render(request, RESET_PASSWORD_TEMPLATE, {
                    "form": form,
                    "token": token,
                    "message": "wrong credentials or token has expired."
                })
            else:
                salt, hashed_token = forgot_case.salt_and_hash.split(":")
                token_checker = hashlib.pbkdf2_hmac('sha256', token.encode('utf-8'), salt.encode('utf-8'), 100000)
                if token_checker.hex() == hashed_token:
                    # SET NEW PASSWORD
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    
                    
                    ForgotPassword.objects.filter(
                        salt_and_hash=forgot_case.salt_and_hash).update(active=False)
                    with open(RESET_CONFIRMATION_EMAIL_TXT, "r") as emailf:
                        emailbody = f"{emailf.read()}".format(first_name=user.first_name)
                    sendemail(
                        sender="aca@agilos.com",
                        password="Agilos123",
                        receiver=user.email,
                        subject=f"{user.first_name}, your password has been reset.",
                        body=emailbody
                    )
                    return render(request, LOGIN_TEMPLATE, {
                        "success": "Password successfully reset."
                    })
                else:
                    return render(request, RESET_PASSWORD_TEMPLATE, {
                        "form": form,
                        "token": token,
                        "message": "Invalid token."
                    })
        else:
            return render(request, RESET_PASSWORD_TEMPLATE, {
                "form": form,
                "token": token
            })


# ----------NORMAL VIEWS----------
@login_required
def home(request):
    return HttpResponse("hello")


@login_required
def sendcase(request):
    if request.method == "POST":
        form = CasesForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user_as_consultant = Consultants.objects.get(user=user)
            form.instance.author = user_as_consultant
            form.save()
            return render(request, HOME_TEMPLATE, {
                "success": "Your case has been successfully sent. Thank you."
            })
        else:
            return render(request, SENDCASE_TEMPLATE, {
                "form": form
            })
    else:
        form = CasesForm()
        return render(request, SENDCASE_TEMPLATE, {
            "form": form
        })


@login_required
def mycases(request):
    if request.method == "GET":
        consultant = Consultants.objects.get(user__username=request.user.username)
        consultant_cases = Cases.objects.filter(author=consultant) # WARNING: IT IS A QUERYSET IN ORDER TO ITERATE OVER IT.
        consultant_last_case = consultant_cases.order_by("-created_at").first()
        consultant_current_year_cases_count = len(consultant_cases.filter(year=timezone.now().year))
        years_desc = list(range(2023, timezone.now().year + 1))[::-1]
        years_desc_test = list(range(2021, timezone.now().year + 1))[::-1]
        current_year = timezone.now().year
        return render(request, MYCASES_TEMPLATE, {
            "cases": consultant_cases,
            "last_case": consultant_last_case,
            "current_year_cases_count": consultant_current_year_cases_count,
            "years_desc": years_desc_test,
            "current_year": current_year
        })


@login_required
def addcertification(request):
    if request.method == "GET":
        form = AddCertificationForm()
        return render(request, ADDCERTIFICATION_TEMPLATE, {
            "form": form
        })
    elif request.method == "POST":
        pass


def mycertifications(request):
    if request.method == "GET":
        return render(request, MYCERTIFICATIONS_TEMPLATE)


