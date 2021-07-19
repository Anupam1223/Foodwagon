from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url

# url name for users url, this will help us to easily find url
app_name = "user"

# path for user related work, when we access 'url:useradd' than the control of
# website will enter UserAdd view similarly with other urls
urlpatterns = [
    path("", views.UserProfile.as_view(), name="userprofile"),
    path("changepassword", views.changePassword, name="changepassword"),
    path("updateuser", views.updateUser, name="updateuser"),
]
