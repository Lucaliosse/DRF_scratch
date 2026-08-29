from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from training.models import Category, Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description", "active", "category"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "date_created", "date_updated", "name", "products"]

    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
            # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise ValidationError("Category already exists")
        return value

    def validate(self, data):
        pass
        # if data['name'] not in data['description']:
        #     raise ValidationError('Name must be in description')
        # return data


class CategoryListSerializer(CategorySerializer):
    pass


class CategoryDetailSerializer(CategorySerializer):

    # By using `SerializerMethodField', we need to implement a
    # 'get_XXX' where XXX is the attribut hame, here 'products'
    products = SerializerMethodField()

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data
