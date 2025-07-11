from django.urls import path
from .views import ProductsView, ContactView, GalleryView, RegisterView, loginView, logoutView, CartView, AddCartItemView, UpdateCartItemView, DeleteCartItemView,SearchProductsView, ClientTestimonialView, ProjectPortfolioView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
    path('products/<int:product_id>/', ProductsView.as_view(), name='product'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('gallery/', GalleryView.as_view(), name='gallery'), 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', loginView.as_view(), name='login'),
    path('logout/', logoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddCartItemView.as_view(), name='add_cart_item'),
    path('cart/update/<int:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/delete/<int:pk>/', DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/search/', SearchProductsView.as_view(), name='products_search'),
    path('testimonials/', ClientTestimonialView.as_view(), name='testimonials'),
    path('portfolio/', ProjectPortfolioView.as_view(), name='portfolio'),
    
]
