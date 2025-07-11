from .models import Products, Contact, Gallery, CartItem, Cart, ClientTestimonial, ProjectPortfolio
from rest_framework import serializers
from django.contrib.auth.models import User


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
        
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery 
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value
    
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save() 
        return user
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'quantity', 'price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
        
class ClientTestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientTestimonial
        fields = '__all__'
        
        
class ProjectPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPortfolio
        fields = '__all__'