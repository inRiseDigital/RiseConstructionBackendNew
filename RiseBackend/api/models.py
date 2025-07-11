from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Products(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    sub_image_1 = models.ImageField(upload_to='products/', null=True, blank=True)
    sub_image_2 = models.ImageField(upload_to='products/', null=True, blank=True)
    sub_image_3 = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Gallery(models.Model):
    title = models.CharField(max_length=100)
    description= models.TextField()
    image = models.ImageField(upload_to='gallery/')
    type=models.CharField(max_length=50, choices=[('residential', 'Residential  '), ('infrastructure', 'Infrastructure'), ('industrial', 'Industrial')], default='image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in {self.cart.user.username}'s cart"
    
    
class ClientTestimonial(models.Model):
    client_name = models.CharField(max_length=255)
    client_feedback = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Assuming a rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"
    
    
class ProjectPortfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
    

    