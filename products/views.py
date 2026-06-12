from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from daraz.permissions import IsAdminOrSeller, IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrSeller]

    filterset_fields = ['category', 'price', 'stock']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        user = self.request.user

        # unauthenticated users see all products
        if not user.is_authenticated:
            return Product.objects.all()

        # seller sees all products publicly
        # but for edit/delete only their own (handled by has_object_permission)
        return Product.objects.all()

    def perform_create(self, serializer):
        # auto assign seller when creating
        serializer.save(seller=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSeller]

    def get_queryset(self):
        # everyone sees all categories
        return Category.objects.all()

    def perform_create(self, serializer):
        # auto assign seller when creating
        serializer.save(seller=self.request.user)


        