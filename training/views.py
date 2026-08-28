from rest_framework.viewsets import ModelViewSet
 
from training.models import Category
from training.serializers import CategorySerializer
 
class CategoryViewset(ModelViewSet):
 
    serializer_class = CategorySerializer
 
    def get_queryset(self):
        return Category.objects.all()