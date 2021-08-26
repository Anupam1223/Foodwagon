from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from .forms import UserAddForm, LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import User as users
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import (
    authenticate,
    login,
)
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

# ------------------------------------------- Create your views here---------------------------
# ------------------ Views for logging in --------------------------
def loginUser(request):
    if not request.session.has_key("user"):
        if request.method == "POST":

            loginForm = LoginForm(request.POST)
            logins = request.POST.get("logins")

            if logins:
                valemail = request.POST.get("username")
                valpassword = request.POST.get("password")
                valRemember = request.POST.get("rememberMe")

                # if user submit empty old password then the program will raise validation error
                if not valemail:
                    data = {"error": "please enter your your email"}
                    return JsonResponse(data)

                # if user submit empty new password then the program will raise validation error
                if not valpassword:
                    data = {"error": "please enter your password"}
                    return JsonResponse(data)

                # if user submit empty new password then the program will raise validation error
                verifyUser = users.objects.filter(email=valemail).first()
                if not verifyUser:
                    data = {"error": "user doesnt exists"}
                    return JsonResponse(data)

                # if user submit empty new password then the program will raise validation error
                if not verifyUser.is_active:
                    data = {"error": "user is not active, check your mail"}
                    return JsonResponse(data)

                # if user submit empty new password then the program will raise validation error
                if not check_password(valpassword, verifyUser.password):
                    data = {"error": "username and  password didnt matched"}
                    return JsonResponse(data)

                user = authenticate(username=valemail, password=valpassword)
                login(request, user)

                # session created
                request.session["user"] = verifyUser.email

                if verifyUser.admin:

                    data = {"success": "admin"}
                    return JsonResponse(data)

                if verifyUser.is_staff:
                    data = {"success": "staff"}
                    return JsonResponse(data)

                data = {"success": "user"}
                return JsonResponse(data)

            else:
                data = {"error": "data cannot be sent, try again"}
                return JsonResponse(data)

        else:
            loginForm = LoginForm()

        return render(request, "sign_in.html", {"form": loginForm})
    else:
        return HttpResponseRedirect("../")


# ------------------------------------------------------------------------------------------------------------


def UserRegister(request):

    if request.method == "POST":

        logins = request.POST.get("logins")

        if logins:
            first_name = request.POST.get("name")
            if not first_name:
                data = {"error": "please enter your name"}
                return JsonResponse(data)

            email = request.POST.get("username")
            if not email:
                data = {"error": "please enter your email"}
                return JsonResponse(data)

            address = request.POST.get("add")
            print("address", address)
            if not address:
                data = {"error": "please enter address"}
                return JsonResponse(data)

            password = request.POST.get("pass1")
            if not password:
                data = {"error": "please enter your password"}
                return JsonResponse(data)

            repassword = request.POST.get("pass2")
            if not repassword:
                data = {"error": "please re-enter password"}
                return JsonResponse(data)

            if repassword != password:
                data = {"error": "re-entered doesnt match"}
                return JsonResponse(data)

            verifyUser = users.objects.filter(email=email).first()
            if verifyUser:
                data = {"error": "email already exists"}
                return JsonResponse(data)

            useradded = users()
            useradded.first_name = first_name
            useradded.email = email
            useradded.password = password
            useradded.set_password(useradded.password)
            useradded.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "acc_active_email.html",
                {
                    "user": useradded,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(useradded.id)),
                    "token": account_activation_token.make_token(useradded),
                },
            )
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            data = {"success": "check mail to verify account"}
            return JsonResponse(data)
        else:
            data = {"error": "data cannot be sent, try again"}
            return JsonResponse(data)
    else:
        useraddform = UserAddForm()

    return render(request, "sign_up.html", {"form": useraddform})


# --------------------------------------------------------------------------------------

# activate your user account after email verification
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = users.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, users.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        users.objects.filter(id=uid).update(is_active=True)
        messages.success(request, "Email verified")
        return redirect(reverse("login:signin"))
    else:
        messages.error(request, "please provide valid email address")
        return redirect(reverse("login:signin"))


# ------------------ function for logout --------------------------
def user_logout(request):
    if request.session.has_key("cart_count") and request.session.has_key(
        "cart_content"
    ):
        del request.session["cart_count"]
        del request.session["cart_content"]
    logout(request)
    return HttpResponseRedirect("../")
