from rest_framework import serializers
from .models import Product, Property


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Property
        fields = (
            "id",
            "owner",
            "content",
            "priority",
            "flag",
            "expireDate",
            "created_at",
        )


class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "content", "priority", "flag")

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'brand', 'rating', 'created_at')


class ProductSearchSerializer(serializers.Serializer):
    category = serializers.CharField()
    brand = serializers.CharField()
    min_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    min_quantity = serializers.IntegerField()
    max_quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    rating = serializers.FloatField()

