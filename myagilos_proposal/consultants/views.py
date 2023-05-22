from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from .forms import AddCertificationForm, CasesForm, ForgotPasswordForm, ResetPasswordForm
from .models import Cases, Consultants, Certification_progress, Consultant_certifications, ForgotPassword, User
from .emailz import *
import hashlib
import os
import secrets

# ----------LOGIN TEMPLATES----------
LOGIN_TEMPLATE = "consultants/logs/login.html"
FORGOT_PASSWORD_TEMPLATE = "consultants/logs/forgot_password.html"
RESET_PASSWORD_TEMPLATE = "consultants/logs/reset_password.html"
SUCCESS_MESSAGE = "Successfully sent. Thank you."
# ----------NORMAL PAGES TEMPLATES----------
HOME_TEMPLATE = "consultants/mains/home.html"
SENDCASE_TEMPLATE = "consultants/mains/sendcase.html"
MYCASES_TEMPLATE = "consultants/mains/mycases.html"
ADDCERTIFICATION_TEMPLATE = "consultants/mains/addcertification.html"
MYCERTIFICATIONS_TEMPLATE = "consultants/mains/mycertifications.html"
# ----------EMAIL TEMPLATES----------
RESET_EMAIL_TXT = "consultants/templates_files/reset_email.txt"
RESET_CONFIRMATION_EMAIL_TXT = "consultants/templates_files/reset_email_confirm.txt"
RECEIVED_CASE_EMAIL_TXT = "consultants/templates_files/received_case_email.txt"
RECEIVED_CERTIFICATION_EMAIL_TXT = "consultants/templates_files/received_certification_email.txt"
MAIL_ENDING = "The MyAgilos Support Team"
# ----------MYAGILOS SUPPORT MAIL----------
MYAGILOS_SUPPORT_MAIL = os.environ.get("MAIL_SENDER")
MYAGILOS_SUPPORT_PASSWORD = os.environ.get("MAIL_PASSWORD")
# ----------RESPONSIBLE USERS----------
MANAGER_MAIL = os.environ.get("MANAGER_MAIL")
MKT_MAIL = os.environ.get("MKT_MAIL")
HR_MAIL = os.environ.get("HR_MAIL")
RESPONSIBLE_USERS = {
    "MANAGER": {
        "MAIL": MANAGER_MAIL,
        "USER": None,
        "FIRST_NAME": None
    },
    "MKT": {
        "MAIL": MKT_MAIL,
        "USER": None,
        "FIRST_NAME": None
    },
    "HR": {
        "MAIL": HR_MAIL,
        "USER": None,
        "FIRST_NAME": None
    }
}
for user in RESPONSIBLE_USERS.items():
    user = user[1]
    try:
        user["USER"] = User.objects.get(email=user["MAIL"])
    except User.DoesNotExist:
        user["USER"] = None
        user["FIRST_NAME"] = None
    else:
        user["FIRST_NAME"] = user["USER"].first_name
# ----------TIME VARIABLES----------
CURRENT_YEAR = timezone.now().year
CURRENT_DATE = timezone.now().date()
CURRENT_DATETIME = timezone.now()


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
                hashed_token = hashlib.pbkdf2_hmac(
                    'sha256', secret_token.encode('utf-8'), salt.encode('utf-8'), 100000)
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
                if MYAGILOS_SUPPORT_MAIL and MYAGILOS_SUPPORT_PASSWORD:
                    sendemail(
                        sender=MYAGILOS_SUPPORT_MAIL,
                        password=MYAGILOS_SUPPORT_PASSWORD,
                        receiver=email,
                        subject=f"{user.first_name}, reset your password",
                        body=body
                    )
                    return HttpResponse(f"Email sent to {email}.")
                else:
                    return HttpResponse("Email not sent: automated mailbox configuration error. Please, contact the IT Support.")
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
                forgot_case = ForgotPassword.objects.get(
                    username=username, active=True, expires_at__gt=current_time)
            except ForgotPassword.DoesNotExist:
                return render(request, RESET_PASSWORD_TEMPLATE, {
                    "form": form,
                    "token": token,
                    "message": "wrong credentials or token has expired."
                })
            else:
                salt, hashed_token = forgot_case.salt_and_hash.split(":")
                token_checker = hashlib.pbkdf2_hmac(
                    'sha256', token.encode('utf-8'), salt.encode('utf-8'), 100000)
                if token_checker.hex() == hashed_token:
                    # SET NEW PASSWORD
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()

                    ForgotPassword.objects.filter(
                        salt_and_hash=forgot_case.salt_and_hash).update(active=False)
                    with open(RESET_CONFIRMATION_EMAIL_TXT, "r") as emailf:
                        emailbody = f"{emailf.read()}".format(
                            first_name=user.first_name)
                    if MYAGILOS_SUPPORT_MAIL and MYAGILOS_SUPPORT_PASSWORD:
                        sendemail(
                            sender=MYAGILOS_SUPPORT_MAIL,
                            password=MYAGILOS_SUPPORT_PASSWORD,
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
    return render(request, HOME_TEMPLATE, {})


@login_required
def sendcase(request):
    if request.method == "POST":
        form = CasesForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user.as_consultant
            form.save()
            received_case_mail_info = {
                "first_name": RESPONSIBLE_USERS["MKT"]["USER"].first_name,
                "sender_first_name": request.user.first_name,
                "sender_last_name": request.user.last_name,
                "company": form.cleaned_data["company"],
                "industry": form.cleaned_data["industry"],
                "project_start": form.cleaned_data["project_end"],
                "project_end": form.cleaned_data["project_end"],
                "issue": form.cleaned_data["issue"],
                "architecture": form.cleaned_data["architecture"],
                "challenge": form.cleaned_data["challenge"],
                "solution": form.cleaned_data["solution"],
                "tools": form.cleaned_data["tools"],
                "why_agilos": form.cleaned_data["why_agilos"],
                "gpt_content": form.cleaned_data["gpt_content"],
                "mail_ending": MAIL_ENDING
            }
            with open(RECEIVED_CASE_EMAIL_TXT, "r") as emailf:
                emailbody = f"{emailf.read()}".format(
                    **received_case_mail_info)
            sendemail(
                sender=MYAGILOS_SUPPORT_MAIL,
                password=MYAGILOS_SUPPORT_PASSWORD,
                receiver=RESPONSIBLE_USERS["MKT"]["MAIL"],
                subject=f"{received_case_mail_info['first_name']}, a new case has been sent.",
                body=emailbody
            )
            return redirect(reverse("consultants:mycases"))
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
def addcertification(request):
    if request.method == "GET":
        certifications = Consultant_certifications.objects.filter(
            consultant=request.user.as_consultant,
            expires_at__lte=CURRENT_DATE
        ).delete()
        form = AddCertificationForm()
        return render(request, ADDCERTIFICATION_TEMPLATE, {
            "form": form
        })
    elif request.method == "POST":
        form = AddCertificationForm(request.POST, request=request)
        if form.is_valid():
            try:
                form.save()
            except ValueError as error:
                return render(request, ADDCERTIFICATION_TEMPLATE, {
                    "form": form,
                    "error": error
                })
            except IntegrityError as error:
                if "unique constraint" in error.args[0].lower():
                    return render(request, ADDCERTIFICATION_TEMPLATE, {
                        "form": form,
                        "error": "Already exists."
                    })
            else:
                received_certification_mail_info = {
                    "sender_first_name": request.user.first_name,
                    "sender_last_name": request.user.last_name,
                    "company": form.cleaned_data["company"],
                    "title": form.cleaned_data["title"],
                    "earned_at": form.cleaned_data["earned_at"],
                    "certifications_from_company": Consultant_certifications.objects.filter(
                        certification__company=form.cleaned_data["company"]
                    ).count(),
                    "this_certification_count": Consultant_certifications.objects.filter(
                        certification__code=form.cleaned_data["title"].split(
                            " - ", 1)[0]
                    ).count(),
                    "mail_ending": MAIL_ENDING
                }
                for USER in RESPONSIBLE_USERS.items():
                    USER = USER[1]
                    received_certification_mail_info["first_name"] = USER["FIRST_NAME"]
                    with open(RECEIVED_CERTIFICATION_EMAIL_TXT, "r") as rf:
                        emailbody = f"{rf.read()}".format(
                            **received_certification_mail_info)
                    sendemail(
                        sender=MYAGILOS_SUPPORT_MAIL,
                        password=MYAGILOS_SUPPORT_PASSWORD,
                        receiver=USER["MAIL"],
                        subject=f"{USER['FIRST_NAME']}, {request.user.first_name} {request.user.last_name} has passed a new certification!",
                        body=emailbody
                    )
                return redirect(reverse("consultants:mycertifications"))
        else:
            return render(request, ADDCERTIFICATION_TEMPLATE, {
                "form": form
            })


@login_required
def mycases(request):
    if request.method == "GET":
        consultant = Consultants.objects.get(
            user=request.user)
        # WARNING: IT IS A QUERYSET IN ORDER TO ITERATE OVER IT.
        consultant_cases = Cases.objects.filter(author=consultant)
        consultant_last_case = consultant_cases.order_by("-created_at").first()
        consultant_current_year_cases_count = len(
            consultant_cases.filter(year=CURRENT_YEAR))
        years_desc = list(range(2023, CURRENT_YEAR + 1))[::-1]
        years_desc_test = list(range(2021, CURRENT_YEAR + 1))[::-1]
        return render(request, MYCASES_TEMPLATE, {
            "cases": consultant_cases,
            "last_case": consultant_last_case,
            "current_year_cases_count": consultant_current_year_cases_count,
            "years_desc": years_desc_test,
            "current_year": CURRENT_YEAR
        })


@login_required
def mycertifications(request):
    three_months_date = CURRENT_DATE + timedelta(days=90)
    if request.method == "GET":
        # CONSULTANT INSTANCE
        consultant = {"instance": Consultants.objects.get(user=request.user)}

        # CERTIFICATIONS
        consultant["certifications"] = consultant["instance"].consultant_certifications_set.filter(
            Q(expires_at__isnull=True) |
            Q(expires_at__gte=CURRENT_DATE)
        ).order_by("-earned_at", "-created_at")
        consultant["certifications"] = [{
            "instance": instance,
            "hurry": True if instance.expires_at and instance.expires_at <= three_months_date else False
        } for instance in consultant["certifications"]]

        # LAST CERTIFICATION
        try:
            consultant["last_certification"] = consultant["certifications"][0]
        except IndexError:
            consultant["last_certification"] = None

        # TARGET
        consultant["target"] = {
            "certification": consultant["instance"].target
        }
        consultant["target"]["achieved"] = Certification_progress.objects.get(
            consultant=consultant["instance"],
            target=consultant["target"]["certification"]
        ).achieved

        return render(request, MYCERTIFICATIONS_TEMPLATE, {
            "certifications": consultant["certifications"],
            "last_certification": consultant["last_certification"],
            "target_certification": consultant["target"]["certification"],
            "target_status": consultant["target"]["achieved"]
        })
