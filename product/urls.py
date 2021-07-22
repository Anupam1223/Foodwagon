from django.contrib import admin
from django.urls import path
from . import views

app_name = "product"
urlpatterns = [
    path("productadd/", views.ProductAdd, name="productadd"),
    path("productread/", views.ProductView.as_view(), name="productread"),
    path("deleteuser/<int:id>/", views.delete_product, name="deleteproduct"),
    path("<int:id>/", views.update_product, name="updateproduct"),
    path("addoffer/", views.add_offer, name="addoffer"),
    path("deleteoffer/<int:id>/", views.delete_offer, name="deleteoffer"),
    path("editoffer/", views.edit_offer, name="editoffer"),
]
