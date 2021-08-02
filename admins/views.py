from product.forms import ProductAddForm
from login.models import User
from product.models import Product
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import (
    AdminAddForm,
    UserUpdateForm,
    UserProfileForm,
    AdditionalInfoForm,
    UserUpdateeForm as showuserform,
    UserUpdateeeForm as userupdateform,
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from product.forms import ProductAddForm
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create AdminView to see user value----------------------------------
class AdminView(TemplateView):
    # this view will render useradd template
    template_name = "admin/useradd.html"

    # when get request is requested by user than this method is runned
    def get(self, request):

        if request.session.has_key("user"):

            semail = request.session["user"]
            verifyUser = User.objects.filter(email=semail).first()

            if verifyUser.admin:
                fm = AdminAddForm()
                additionalinfo = AdditionalInfoForm()
                # rendering the userview template to see them
                return render(
                    request,
                    self.template_name,
                    {"form": fm, "additional": additionalinfo},
                )
            else:
                fm = ProductAddForm()
                # rendering the userview template to see them
                return render(request, "admin/productadd.html", {"form": fm})

        else:
            return HttpResponseRedirect("../login/")


# Admin Add helps admin to add the user as admin--------------------------------------------------
def AdminAdd(request):

    if request.session.has_key("user"):

        # extract session value to extract the user password from database
        semail = request.session["user"]

        # extract the user with matching email taken from session
        verifyUser = User.objects.filter(email=semail).first()
        if verifyUser.admin:

            if request.method == "POST":
                useraddform = AdminAddForm(
                    data=(request.POST or None), files=(request.FILES or None)
                )

                if useraddform.is_valid():

                    pw = useraddform.cleaned_data["password"]
                    useradded = useraddform.save(commit=False)
                    useradded.set_password(useradded.password)
                    useradded.save()

                    trader_email = useraddform.cleaned_data["email"]
                    trader = User.objects.filter(email=trader_email).first()
                    if trader.is_staff:
                        userextrainfo = AdditionalInfoForm(
                            data=(request.POST or None), files=(request.FILES or None)
                        )
                        extrainfo = userextrainfo.save(commit=False)
                        extrainfo.user = trader
                        extrainfo.save()

                    current_site = get_current_site(request)
                    mail_subject = "Activate your account."
                    message = render_to_string(
                        "acc_for_vendor.html",
                        {
                            "user": useradded,
                            "domain": current_site.domain,
                            "username": useradded.email,
                            "password": pw,
                        },
                    )
                    to_email = useradded.email
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()

                    messages.success(
                        request, "User added sucessfully, email is sent to the trader"
                    )
                    return HttpResponseRedirect("../admins/admin")
                else:
                    print("invalid form")
            else:
                useraddform = AdminAddForm()
            return render(request, "admin/useradd.html", {"form": useraddform})
        else:
            return HttpResponseRedirect("../admins/admins/")
    else:
        return HttpResponseRedirect("../login/")


# Create UserView to see user value
class AdminUserView(TemplateView):
    # this view will render userread template
    template_name = "admin/userread.html"

    # when get request is requested by user than this method is runned
    def get(self, request):
        # select all the data from user to render in userview
        user = User.objects.all()
        paginator = Paginator(user, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # rendering the userview template to see them
        return render(request, self.template_name, {"users": page_obj})


# user with admin access can delete other user
def DeleteUser(request, id):
    if request.method == "POST":
        userstatus = User.objects.filter(id=id).first()
        product = Product.objects.filter(trader=userstatus.id)
        if userstatus.is_active == True:

            User.objects.filter(id=id).update(is_active=False)
            for products in product:
                Product.objects.filter(id=products.id).update(status=False)

            messages.success(request, "user disabled")
            return HttpResponseRedirect("../../userread")
        else:
            User.objects.filter(id=id).update(is_active=True)
            messages.success(request, "user activated")
            return HttpResponseRedirect("../../userread")

    return HttpResponseRedirect("../admins")


# user with admin access can update other user
def UpdateUser(request, id):
    if request.method == "POST":
        data = User.objects.get(pk=id)
        fm = UserUpdateForm(request.POST, instance=data)
        if fm.is_valid():
            fm.save()
            messages.success(request, "user updated sucessfully")
            return HttpResponseRedirect("../userread")
        else:
            return render(request, "admin/updateuser.html", {"form": fm})
    data = User.objects.get(pk=id)
    fm = UserUpdateForm(instance=data)

    return render(request, "admin/updateuser.html", {"form": fm})


# ChangePass view will take in the request body with old and new password
def ChangePass(request):
    if request.method == "POST":

        fpassword = request.POST.get("oldPass")

        password1 = request.POST.get("newPass1")

        password2 = request.POST.get("newPass2")

        # if user submit empty old password then the program will raise validation error
        if not fpassword:
            messages.error(request, "please enter OLD PASSWORD")
            return HttpResponseRedirect("../admin")

        # if user submit empty new password then the program will raise validation error
        if not password1:
            messages.error(request, "please enter NEW PASSWORD")
            return HttpResponseRedirect("../admin")

        # if user submit empty new re-password then the program will raise validation error
        if not password2:
            messages.error(request, "please re-enter NEW PASSWORD")
            return HttpResponseRedirect("../admin")

        # extract session value to extract the user password from database
        semail = request.session["user"]

        # extract the user with matching email taken from session
        verifyUser = User.objects.filter(email=semail).first()

        # userid of extracted user
        userid = verifyUser.id

        # password of extracted pasword
        userpass = verifyUser.password

        print(userpass, fpassword)

        # checks whether the password given by user and actual password matches or not
        if check_password(fpassword, userpass):
            # checks whether the new password matches
            if password1 == password2:

                password_to_save = make_password(password2)
                # update the passowrd
                User.objects.filter(id=userid).update(password=password_to_save)
                # if updated than message is shown in the dashboard
                messages.success(request, "password updated successfully")
                return HttpResponseRedirect("/login/")

            else:
                messages.error(request, "reenter password didnt matched")
                return HttpResponseRedirect("../admin")
        else:
            messages.error(request, "old password didnt matched")
            return HttpResponseRedirect("../admin")


# change profile image
def Profile(request, id):
    if request.method == "POST":
        datas = User.objects.get(pk=id)
        fm = UserProfileForm(
            data=(request.POST or None), files=(request.FILES or None), instance=datas
        )
        if fm.is_valid():
            fm.save()
        else:
            print("invalid form")

    datas = User.objects.get(pk=id)
    fm = UserProfileForm(instance=datas)

    return render(request, "admin/admin_profile.html", {"form": fm})


# working on user----------------------------------------------------


# Create UserView to see user value----------------------------------
class UserProfile(TemplateView):
    # this view will render userread template
    template_name = "user/user_profile.html"

    # when get request is requested by user than this method is runned
    def get(self, request):
        if request.session.has_key("user"):
            fm = showuserform()
            if request.session.has_key("cart_count"):
                no_of_item_in_cart = request.session["cart_count"]
            else:
                no_of_item_in_cart = None
            # rendering the userview template to see them
            return render(
                request,
                self.template_name,
                {
                    "form": fm,
                    "cart_count": no_of_item_in_cart,
                },
            )
        else:
            return HttpResponseRedirect("../login/")


# ---------------------------------------------------------------------

# user with admin access can update other user
def ChangeCustomerPassword(request):
    if request.method == "POST":

        fpassword = request.POST.get("pass")

        password1 = request.POST.get("pass1")

        password2 = request.POST.get("pass2")

        # if user submit empty old password then the program will raise validation error
        if not fpassword:
            data = {"error": "please enter your old password"}
            return JsonResponse(data)

        # if user submit empty new password then the program will raise validation error
        if not password1:
            data = {"error": "please enter new password"}
            return JsonResponse(data)

        # if user submit empty new re-password then the program will raise validation error
        if not password2:
            data = {"error": "please re-enter new password"}
            return JsonResponse(data)

        # extract session value to extract the user password from database
        semail = request.session["user"]

        # extract the user with matching email taken from session
        verifyUser = User.objects.filter(email=semail).first()

        # userid of extracted user
        userid = verifyUser.id
        # password of extracted pasword
        userpass = verifyUser.password

        # checks whether the password given by user and actual password matches or not
        if check_password(fpassword, userpass):
            # checks whether the new password matches
            if password1 == password2:

                password_to_save = make_password(password2)
                # update the passowrd
                User.objects.filter(id=userid).update(password=password_to_save)
                # if updated than message is shown in the dashboard
                data = {"success": "password changed successfully"}
                return JsonResponse(data)
            else:
                data = {"error": "re-entered password didnt matched"}
                return JsonResponse(data)
        else:
            data = {"error": "old password didnt matched"}
            return JsonResponse(data)


# user with admin access can update other user
def UpdateCustomerUser(request):
    if request.method == "POST":

        # extract session value to extract the user password from database
        semail = request.session["user"]

        # extract the user with matching email taken from session
        verifyUser = User.objects.filter(email=semail).first()

        # userid of extracted user
        userid = verifyUser.id

        datas = User.objects.get(pk=userid)

        fm = userupdateform(
            data=(request.POST or None), files=(request.FILES or None), instance=datas
        )

        if fm.is_valid():
            fm.save()
            messages.success(request, "user updated successfully")
            return HttpResponseRedirect("../admins/userprofile")
        else:
            messages.error(request, "user update unsuccessfull")
            return HttpResponseRedirect("../admins/userprofile")
