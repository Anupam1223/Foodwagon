from django.contrib import admin
from django.urls import path
from . import views

# url name for users url, this will help us to easily find url
app_name = "admins"

# path for user related work, when we access 'url:useradd' than the control of
# website will enter UserAdd view similarly with other urls
urlpatterns = [
    path("admin", views.AdminView.as_view(), name="admins"),
    path("addadmin", views.AdminAdd, name="addadmin"),
    path("userread/", views.AdminUserView.as_view(), name="userread"),
    path("deleteuser/<int:id>/", views.DeleteUser, name="deleteuser"),
    path("<int:id>/", views.UpdateUser, name="updateuser"),
    path("changePass/", views.ChangePass, name="changepass"),
]
