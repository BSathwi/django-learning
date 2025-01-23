from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.permissions import IsAuthenticated


class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API view to handle product creation and listing.
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        category_id = request.data.get('category')
        try:
            category = Category.objects.get(id=category_id) 
        except Category.DoesNotExist:
            return Response({"error": "Invalid category ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_data = request.data
        product_data['category'] = category.id
        
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save(category=category)
            return Response({"message": "Product created successfully!",'data':serializer}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API view to handle category creation.
    """
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message": "Category created successfully!",
                "category": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

class GetProductById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        

class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API view to update product details.
    """
    def put(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Product updated successfully!",
                "product": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    """
    API view to delete a product.
    """
    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            return Response({"message": "Product deleted successfully!"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class SearchProductView(APIView):
    """
    API view to search products by name or category.
    """
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(category__name__icontains=query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
