import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Products, Contact, Gallery, Cart, CartItem, ClientTestimonial, ProjectPortfolio
from .serializer import ProductsSerializer, ContactSerializer, GallerySerializer, UserSerializer, CartItemSerializer, CartSerializer, ClientTestimonialSerializer, ProjectPortfolioSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated



# Create your views here.

class ProductsView(APIView):
        def get(self, request, product_id=None):
            if product_id:
                product = get_object_or_404(Products, id=product_id)
                serializer = ProductsSerializer(product)
            else:
                products = Products.objects.all()
                serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    

class GalleryView(APIView):
    def get(self, request):
        gallery = Gallery.objects.all()
        serializer = GallerySerializer(gallery, many=True)
        return Response(serializer.data)
    
class ClientTestimonialView(APIView):
    def get(self, request):
        testimonials = ClientTestimonial.objects.all()
        serializer = ClientTestimonialSerializer(testimonials, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ClientTestimonialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user_id': user.id,
                'username': user.username,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class loginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.id,
                'username': user.username,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class logoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Add item to the user's cart
        product_name = request.data.get('product_name')
        quantity = request.data.get('quantity')
        price = request.data.get('price')

        if not all([product_name, quantity, price]):
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        cart_item = CartItem.objects.create(cart=cart, product_name=product_name, quantity=quantity, price=price)
        item_serializer = CartItemSerializer(cart_item)

        return Response(item_serializer.data, status=status.HTTP_201_CREATED)

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # Update an existing cart item
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.product_name = request.data.get('product_name', cart_item.product_name)
        cart_item.quantity = request.data.get('quantity', cart_item.quantity)
        cart_item.price = request.data.get('price', cart_item.price)

        cart_item.save()

        item_serializer = CartItemSerializer(cart_item)
        return Response(item_serializer.data, status=status.HTTP_200_OK)

class DeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Remove an item from the user's cart
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"detail": "Cart item removed."}, status=status.HTTP_204_NO_CONTENT)
    
class SearchProductsView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        if not query:
            return Response({"detail": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        products = Products.objects.filter(title__icontains=query)
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    
class ProjectPortfolioView(APIView):
    def get(self, request):
        projects = ProjectPortfolio.objects.all()
        serializer = ProjectPortfolioSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    