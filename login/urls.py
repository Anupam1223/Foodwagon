from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path("", views.loginUser, name="signin"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.UserRegister, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]