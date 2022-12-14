from decimal import Decimal
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, When, Case, Q
from business.serializers.transaction_serializer import CheckoutSerializer

from business.models import UserCartProduct, UserCart


class CheckOutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserCartProduct.objects.all()
    serializer_class = CheckoutSerializer

    def get(self, request):
        try:
            user = request.user
            cart = UserCart.objects.filter(user=user)
            if not cart.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": "user has no products registered"
                    }
                    , status=status.HTTP_400_BAD_REQUEST
                )
            user_cart = cart.first()
            serializer = self.get_serializer(user_cart)
            return Response(
                {
                    "message": "Success",
                    "data": serializer.data,
                    "errors": "null"
                }
                , status=status.HTTP_400_BAD_REQUEST
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
