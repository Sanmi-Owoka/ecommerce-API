from rest_framework import serializers
from business.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=68, min_length=3)
    category = serializers.ChoiceField(choices=[
        "groceries", "accessories",
        "laundry_products", "books",
        "stationeries", "drinks",
        "sea_food", "snacks"
    ])
    size = serializers.CharField(max_length=68, min_length=3, allow_blank=False)
    color = serializers.CharField(max_length=68, min_length=3, allow_blank=False)
    quantity = serializers.IntegerField(max_value=1000000, min_value=1)
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    cover_image = serializers.ImageField(allow_empty_file=False, use_url=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = [
            "id",
            "updated_at",
            "created_at"
        ]

    def validate(self, attrs):
        name = attrs.get("name", "")
        if Product.objects.filter(name=name).exists():
            raise serializers.ValidationError({"email": f"Product with name: {name} already exists"})
        return attrs

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.size = validated_data.get('size', instance.size)
        instance.color = validated_data.get('color', instance.color)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.cover_image = validated_data.get('cover_image', instance.cover_image)
        return instance

class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = [
            "id",
            "name",
            "category",
            "size",
            "color",
            "quantity",
            "price",
            "cover_image",
            "updated_at",
            "created_at"
        ]
