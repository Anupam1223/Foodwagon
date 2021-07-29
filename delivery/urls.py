from django.urls import path
from . import views

app_name = "delivery"
urlpatterns = [
    path("", views.CategoryView.as_view(), name="delivery"),
    path("filter/", views.filter_category, name="filter"),
    path("productpage/<int:id>", views.filter_product, name="productpage"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
]
