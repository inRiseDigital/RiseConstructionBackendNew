from django.contrib import admin
from .models import Products, Contact, Gallery, Cart, CartItem, ClientTestimonial

# Register your models here.

admin.site.register(Products)   
admin.site.register(Contact)
admin.site.register(Gallery)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ClientTestimonial)

