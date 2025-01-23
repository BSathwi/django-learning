from django.urls import path
from .views import ProductView,CategoryCreateView,GetProductById,UpdateProductView,DeleteProductView,SearchProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('categories/', CategoryCreateView.as_view(), name='create-category'),
    path('products/<int:pk>/', GetProductById.as_view(), name='get-product-by-id'),
    path('products/update/<int:pk>/', UpdateProductView.as_view(), name='update-product'),
    path('products/delete/<int:pk>/', DeleteProductView.as_view(), name='delete-product'),
    path('products/search/', SearchProductView.as_view(), name='search-products'),

]
