from django.db import models
from merchant.models import MerchantUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Shop(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    merchant = models.ForeignKey(MerchantUser,on_delete=models.CASCADE)

    

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} --- {self.shop}'
    

    

class ConnectedShop(models.Model):
    STATUS_CHOICES = (
        ('PENDING','Pending'),
        ('REJECT','Rejected'),
        ('ACCEPT','Accepted')
    )
    sender_shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='sender')
    receiver_shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='receiver')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')

    def __str__(self):
        return self.status
    

class Cart(models.Model):
    shop = models.OneToOneField(Shop,on_delete=models.CASCADE)

    def __str__(self):
        return self.shop.name


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name}:{self.quentity}'
    def unite_price(self):
        return self.product.price
    @property
    def total_price(self):
        return self.product.price*self.quentity
    
# class Order(models.Model):
#     shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
#     cart_total_price = models.DecimalField(max_digits=10,decimal_places=2)
#     merchant = models.ForeignKey(MerchantUser,on_delete=models.CASCADE)


class Order(models.Model):
    shop_name = models.CharField(max_length=200)
    #cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    cart_total_price = models.DecimalField(max_digits=10,decimal_places=2)
    merchant = models.ForeignKey(MerchantUser,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)