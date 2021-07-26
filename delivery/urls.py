from django.urls import path
from . import views

app_name = "delivery"
urlpatterns = [
    path("", views.CategoryView.as_view(), name="delivery"),
    path("viewalltrader", views.VendorView.as_view(), name="viewalltrader"),
]
