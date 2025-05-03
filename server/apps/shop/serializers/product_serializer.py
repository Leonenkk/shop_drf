from django.core.validators import MinValueValidator
from rest_framework import serializers

from apps.shop.models import Product, ProductImages, Category
from apps.shop.serializers import CategorySerializer


class SellerShopSerializer(serializers.Serializer):
    name=serializers.CharField(source='business_name')
    slug=serializers.SlugField()
    avatar=serializers.SerializerMethodField()

    def get_avatar(self,obj)->str|None:
        request=self.context.get('request')
        if not obj.user.avatar:
            return None
        return request.build_absolute_uri(obj.user.avatar.url) if request else obj.user.avatar.url

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImages
        fields=(
            'image',
            'order'
        )
        read_only_fields=('order',)


class ProductSerializer(serializers.ModelSerializer):
    seller=SellerShopSerializer()
    category=CategorySerializer()
    images=ProductImagesSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model=Product
        fields=(
            'name',
            'slug',
            'description',
            'price_old',
            'price_current',
            'in_stock',
            'seller',
            'category',
            'images',
        )
        read_only_fields=('slug',)

class ProductCreateSerializer(serializers.ModelSerializer):
    category_slug=serializers.CharField(write_only=True)
    images=serializers.ListField(
        child=serializers.ImageField(),
        min_length=1,
        write_only=True,
        required=True,
    )
    class Meta:
        model=Product
        fields=(
            'name',
            'description',
            'price_current',
            'in_stock',
            'category_slug',
            'images'
        )
        extra_kwargs={
            'price_current': {
                'validators': [MinValueValidator(0.0)],
            }
        }

    def create(self, validated_data):
        seller=self.context['seller']
        category_slug=validated_data.pop('category_slug')
        images=validated_data.pop('images')
        category=Category.objects.get_or_none(slug=category_slug)
        if not category:
            raise serializers.ValidationError('There is no such category')
        product=Product.objects.create(
            category=category,
            seller=seller,
            **validated_data
        )
        for order,image in enumerate(images,start=1):
            ProductImages.objects.create(
                product=product,
                order=order,
                image=image,
            )
        return product

    def update(self, instance, validated_data):#instance - текущее сост, validated_data-новое
        if 'price_current' in validated_data:
            if validated_data['price_current'] != instance.price_current:
                validated_data['price_old']=instance.price_current
        if 'category_slug' in validated_data:
            category_slug=validated_data.pop('category_slug')
            category=Category.objects.get_or_none(slug=category_slug)
            if not category:
                raise serializers.ValidationError('There is no such category')
            instance.category=category
        if 'images' in validated_data:
            instance.images.all().delete()
            images=validated_data.pop('images')
            for order,image in enumerate(images,start=1):
                ProductImages.objects.create(
                    product=instance,
                    order=order,
                    image=image,
                )
        return super().update(instance, validated_data)

