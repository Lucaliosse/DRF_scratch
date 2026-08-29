from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from training.models import Category, Product
from training.serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductSerializer,
)


class CategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter()

    def get_serializer_class(self):
        # Get single item -> use detail serializer
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProductViewset(ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get("category_id")
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset
