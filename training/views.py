from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from training.models import Category, Product
from training.serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductSerializer,
)


class CategoryViewset(ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter()

    def get_serializer_class(self):
        # Get single item -> use detail serializer
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def disable(self, request, pk=None):
        category = self.get_object()
        category.active = False
        category.save()

        category.products.all().update(active=False)

        return Response(
            {
                "message": f"Category '{category.name}' and all its products have been disabled."
            },
            status=status.HTTP_200_OK,
        )


class ProductViewset(ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get("category_id")
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset
