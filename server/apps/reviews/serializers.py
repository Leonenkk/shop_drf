from rest_framework import serializers

from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field="slug",
    )

    class Meta:
        model = Review
        fields = (
            "user",
            "product",
            "rating",
            "text",
            "average_rating",
            "id",
        )
        read_only_fields = ("user", "average_rating", "product", "id")

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data.get("product")
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Product must have only one review")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product = validated_data.get("product")
        if product and instance.product != product:
            raise serializers.ValidationError(
                "You can't change the product of the review"
            )
        return super().update(instance, validated_data)
