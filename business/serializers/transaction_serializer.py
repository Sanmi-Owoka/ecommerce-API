from rest_framework import serializers
from business.models import UserCartProduct

class DebitUserSerializer(serializers.ModelSerializer):
    user_balance = serializers.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        model = UserCartProduct
        fields = ['user_balance',]