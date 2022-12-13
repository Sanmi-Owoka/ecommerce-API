from rest_framework import serializers
from business.models import UserCartProduct, UserCart
from .product_serializer import GetProductSerializer
from users.serializers.authentication_serializers import UserSerializer


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = "__all__"


class UserCartProductSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = GetProductSerializer()
    cart = UserCartSerializer()

    class Meta:
        model = UserCartProduct
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "product",
            "cart",
            "total_amount"
        ]


class RegisterUserCartProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=68, min_length=3)
    quantity = serializers.IntegerField(max_value=1000000, min_value=1)

    class Meta:
        model = UserCartProduct
        fields = [
            "product_name",
            "quantity",
        ]


class DeleteUserCartProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=68, min_length=3)

    class Meta:
        model = UserCartProduct
        fields = [
            "product_name",
        ]
