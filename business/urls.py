from django.urls import path
from .views.cart_view import CartView, DeleteCartView, ClearCartProductsViews
from .views.transaction_views import CheckOutView

urlpatterns = [
    path("register/product/", CartView.as_view(), name="register product to cart"),
    path("delete/product/<str:product_name>/", DeleteCartView.as_view(), name="delete product from cart"),
    path("clear/products/", ClearCartProductsViews.as_view(), name="clear user's cart"),
    path("checkout/", CheckOutView.as_view(), name="pay for products"),
]
