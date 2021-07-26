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
    path("addcategory/", views.add_category, name="addcategory"),
    path("viewcategory/", views.category_view.as_view(), name="viewcategory"),
    path("updatecategory/<int:id>/", views.update_category, name="updatecategory"),
]
