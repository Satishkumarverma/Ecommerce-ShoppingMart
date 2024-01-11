from django.contrib import admin
from app_version1.models import Customer, Product, Cart, OrderPlaced

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'locality', 'city', 'zipcode', 'state')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling_price', 'discounted_price', 'discription', 'brand', 'category', 'product_image')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'Customer', 'product', 'quantity', 'order_date', 'status')            
