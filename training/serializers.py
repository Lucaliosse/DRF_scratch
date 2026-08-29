from rest_framework.serializers import ModelSerializer, SerializerMethodField

from training.models import Category, Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "active", "category"]


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "date_created", "date_updated", "name", "products"]


class CategoryDetailSerializer(ModelSerializer):

    # By using `SerializerMethodField', we need to implement a
    # 'get_XXX' where XXX is the attribut hame, here 'products'
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "date_created", "date_updated", "name", "products"]

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data
