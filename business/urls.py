from django.urls import path
from .views.cart_view import CartView, DeleteCartView


urlpatterns = [
    path("register/product/", CartView.as_view(), name="register product to cart"),
    path("delete/product/<str:product_name>", DeleteCartView.as_view(), name="delete product from cart"),
]