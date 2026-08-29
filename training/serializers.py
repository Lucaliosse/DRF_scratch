from rest_framework.serializers import ModelSerializer

from training.models import Category, Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "active", "category"]


class CategorySerializer(ModelSerializer):

    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "date_created", "date_updated", "name", "products"]
