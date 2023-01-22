from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        "auth.User", related_name="Property", null=True, on_delete=models.CASCADE
    )
    content = models.TextField()
    priority = models.TextField()
    flag = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expireDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        super().save(*args, **kwargs)


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial')
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=255)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    valid_sort_fields = ['name', 'category', 'brand', 'rating', 'price', 'quantity', 'created_at']


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
