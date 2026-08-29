from rest_framework.viewsets import ModelViewSet
from training.models import Category, Product
from training.serializers import CategorySerializer, ProductSerializer


class CategoryViewset(ModelViewSet):

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter()


class ProductViewset(ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get("category_id")
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset
