from decimal import Decimal
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, When, Case, Q
from rest_framework.viewsets import ModelViewSet
from business.models import UserCartProduct, UserCart, Product
from business.serializers.cart_serializer import (
    UserCartProductSerializer, 
    RegisterUserCartProductSerializer, 
    DeleteUserCartProductSerializer
)
from business.serializers.product_serializer import GetProductSerializer


class CartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserCart.objects.all()
    serializer_class = RegisterUserCartProductSerializer

    
    def post(self, request):
        try:
            user = request.user
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors,
                    }
                    , status=status.HTTP_400_BAD_REQUEST)

            product_name = serializer.validated_data["product_name"]
            quantity = serializer.validated_data["quantity"]
            product_queryset = Product.objects.filter(name=product_name)
            if not product_queryset.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"product with name: {product_name} does not exist",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            product = product_queryset.first()
            price = product.price
            product_quantity = product.quantity
            if product_quantity <= 0:
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"product with name: {product_name} is out of stock",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            
            if quantity > product_quantity :
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"""the quantity entered is greater than the product quantity, the current product quantity is {product_quantity }""",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            user_cart, created = UserCart.objects.get_or_create(user=user)
            amount = Decimal(float(price)) * int(quantity)
            check_user_cart_product_queryset = UserCartProduct.objects.filter(
                user=user, 
                product=product,
                cart=user_cart
                )
            if check_user_cart_product_queryset.exists():
                user_cart_product = check_user_cart_product_queryset.first()
                previous_amount = user_cart_product.total_amount
                previous_quantity = user_cart_product.quantity
                user_cart_product.total_amount = previous_amount + amount
                user_cart_product.quantity = previous_quantity + quantity
                user_cart_product.save()
                product.quantity = product_quantity - quantity
                product.save()
            else:
                user_cart_product = UserCartProduct.objects.create(
                    user=user,
                    product=product,
                    quantity=quantity,
                    total_amount=amount,
                    cart=user_cart
                )
                product.quantity = product_quantity - quantity
                product.save()
            response = UserCartProductSerializer(user_cart_product)
            return Response(
                {
                        "message": "Success",
                        "data": response.data,
                        "errors": "null"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("error", e)
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": [f"{e}"]
                }
                , status=status.HTTP_400_BAD_REQUEST
            )

class DeleteCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserCart.objects.all()
    serializer_class = DeleteUserCartProductSerializer

    def delete(self, request, product_name):
        try:
            user = request.user
            product_queryset = Product.objects.filter(name=product_name)
            if not product_queryset.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"product with name: {product_name} does not exist",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            product = product_queryset.first()
            get_user_cart_queryset = UserCart.objects.filter(user=user)
            if not get_user_cart_queryset.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": "user does not have any recorded products in cart",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            user_cart = get_user_cart_queryset.first()
            check_user_cart_product_queryset = UserCartProduct.objects.filter(
                user=user, 
                product=product,
                cart=user_cart
                )
            if not check_user_cart_product_queryset.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"user has no {product_name} registered",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)
            user_cart_product = check_user_cart_product_queryset.first()
            new_quantity = user_cart_product.quantity + product.quantity
            product.quantity = new_quantity
            product.save()
            user_cart_product.delete()
            response = GetProductSerializer(product)
            return Response(
                    {
                        "message": "Success",
                        "data": response.data,
                        "errors": f"null",
                    }
                    , status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("error", e)
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": [f"{e}"]
                }
                , status=status.HTTP_400_BAD_REQUEST
            )