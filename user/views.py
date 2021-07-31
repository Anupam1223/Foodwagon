from login.models import User
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import UserUpdateForm, UserUpdateeForm, AdminAddForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse

# Create UserView to see user value----------------------------------
class UserProfile(TemplateView):
    # this view will render userread template
    template_name = "user/user_profile.html"

    # when get request is requested by user than this method is runned
    def get(self, request):
        if request.session.has_key("user"):
            fm = UserUpdateForm()
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
def changePassword(request):
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
def updateUser(request):
    if request.method == "POST":

        # extract session value to extract the user password from database
        semail = request.session["user"]

        # extract the user with matching email taken from session
        verifyUser = User.objects.filter(email=semail).first()

        # userid of extracted user
        userid = verifyUser.id

        datas = User.objects.get(pk=userid)

        fm = UserUpdateeForm(
            data=(request.POST or None), files=(request.FILES or None), instance=datas
        )

        if fm.is_valid():
            fm.save()
            messages.success(request, "user updated successfully")
            return HttpResponseRedirect("../user")
        else:
            print("invalid form")
            messages.error(request, "user update unsuccessfull")
            return HttpResponseRedirect("../user")
