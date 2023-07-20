from django.contrib import admin
from .models import Category, Order, Shop,Product,ConnectedShop, Cart, CartItem
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Category)
admin.site.register(Order)


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ['id','cart','product','unite_price','quentity','total_price']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','shop']
    # fieldsets = [
    #     ('Shop Name', {"fields": ["name"]}),
    #     ('ForignKey FIelds',{"fields":['merchant','categoty']}),
    #     ("Activaty", {"fields": ["is_active"]}),
       
    # ]
admin.site.register(Cart,CartAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id','name','is_active','category','merchant']
    fieldsets = [
        ('Shop Name', {"fields": ["name"]}),
        ('ForignKey FIelds',{"fields":['merchant','category']}),
        ("Activaty", {"fields": ["is_active"]}),
       
    ]
admin.site.register(Shop,ShopAdmin)


class ConnectedShopAdmin(admin.ModelAdmin):
    list_display = ['id','sender_shop','receiver_shop','status']
admin.site.register(ConnectedShop,ConnectedShopAdmin)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','name','price']