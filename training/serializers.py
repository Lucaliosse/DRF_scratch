from rest_framework.serializers import ModelSerializer

from training.models import Category, Product


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "description", "active"]


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "active", "category"]
