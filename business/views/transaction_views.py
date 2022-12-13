from decimal import Decimal
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, When, Case, Q
from business.serializers.transaction_serializer import DebitUserSerializer

from business.models import UserCartProduct, UserCart

class BuyProductsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserCartProduct.objects.all()
    serializer_class = DebitUserSerializer

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
            check_user_products = self.queryset.filter(user=user, cart=user_cart).aggregate(Sum("total_amount"))
            total_amount = (
                0
                if check_user_products["total_amount__sum"] is None
                else check_user_products["total_amount__sum"]
            )
            print(total_amount)
            user_balance = serializer.validated_data["user_balance"]
            if total_amount > user_balance:
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"user balance is {user_balance} which is less than the total amount of {total_amount} "
                    }
                    , status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {
                        "message": "Success",
                        "data": "products have been paid for successfully",
                        "errors": "null"
                    }
                    , status=status.HTTP_200_OK
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