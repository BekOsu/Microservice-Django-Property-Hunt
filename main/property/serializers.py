from rest_framework import serializers
from property.models import Property


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


class PropertyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ("id", "content", "priority", "flag")

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Property.objects.create(**validated_data)
