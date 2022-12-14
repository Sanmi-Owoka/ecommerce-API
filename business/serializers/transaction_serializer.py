from rest_framework import serializers
from business.models import UserCartProduct, UserCart
from django.db.models import Sum


class UserProductSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = UserCartProduct
        fields = [
            "product_name",
            "quantity",
            "total_amount",
            "product_price"
        ]

    def get_product_name(self, instance):
        try:
            return instance.product.name
        except Exception as e:
            print("error", e)
            return None

    def get_product_price(self, instance):
        try:
            return instance.product.price
        except Exception as e:
            print("error", e)
            return None


class CheckoutSerializer(serializers.ModelSerializer):
    cart_products = serializers.SerializerMethodField()
    total_amount_to_be_paid = serializers.SerializerMethodField()

    class Meta:
        model = UserCart
        fields = [
            "cart_products",
            "total_amount_to_be_paid",
        ]
        read_only_fields = [
            "cart_products",
            "total_amount_to_be_paid",
        ]

    def get_cart_products(self, instance):
        try:
            user = instance.user
            user_cart = instance
            all_cart_products = UserCartProduct.objects.filter(user=user, cart=user_cart)
            if not all_cart_products.exists():
                return []
            else:
                serializer = UserProductSerializer(all_cart_products, many=True)
                return serializer.data
        except Exception as e:
            print("error", e)
            return None

    def get_total_amount_to_be_paid(self, instance):
        try:
            user = instance.user
            user_cart = instance
            check_user_products = UserCartProduct.objects.filter(user=user, cart=user_cart).aggregate(
                Sum("total_amount"))
            total_amount = (
                0
                if check_user_products["total_amount__sum"] is None
                else check_user_products["total_amount__sum"]
            )
            return total_amount
        except Exception as e:
            print("error", e)
            return None
