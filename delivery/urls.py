from django.urls import path
from . import views

app_name = "delivery"
urlpatterns = [
    path("", views.CategoryView.as_view(), name="delivery"),
    path("filter/", views.filter_category, name="filter"),
    path("productpage/<int:id>", views.filter_product, name="productpage"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove_from_cart/", views.remove_from_cart, name="remove_from_cart"),
    path("add_to_order/", views.add_to_order, name="add_to_order"),
    path("view_order/", views.View_Order.as_view(), name="view_order"),
    path("view_bill/<int:id>", views.view_bill, name="view_bill"),
    path("download_file/<int:id>", views.generatePDF, name="download_file"),
]
