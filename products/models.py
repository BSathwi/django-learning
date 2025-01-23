from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    """
    Model for product categories.
    """
    name = models.CharField(max_length=255, unique=True)  # Category name, unique to avoid duplicates

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Model for storing product details.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = CloudinaryField('image')
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
