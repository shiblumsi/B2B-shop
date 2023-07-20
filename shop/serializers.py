from rest_framework import serializers
from .models import Cart, CartItem, Category, Order, Shop, Product, ConnectedShop


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ShopCreateSerializer(serializers.ModelSerializer):
    merchant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #category = serializers.StringRelatedField()
    class Meta:
        model = Shop
        fields = ['name','category','is_active','merchant']
        

class ShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        exclude = ['merchant']
        depth =1


class ShopRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ''

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ShopDetailSerializer(serializers.ModelSerializer):
    #products = serializers.SerializerMethodField()
    #product = ProductSerializer()
    class Meta:
        model = Shop
        fields = ['id','name']

    def get_products(self, obj):
        return obj
    
class ShopProductAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name','price']

    # def create(self, validated_data):
    #     print('fffffffffffffffffffff',validated_data)
    #     return Product.objects.create(**validated_data)

class ShopProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class SameCategoryShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ConnectedShopSerializer(serializers.ModelSerializer):
    receiver_shop = ShopsSerializer()
    class Meta:
        model = ConnectedShop
        fields = ['id','receiver_shop']

class ConnectedShopProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price']


class ConnectionRequestSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedShop
        fields = ['receiver_shop']

    # def create(self, validated_data):
    #     print('vvvvvvvvvvvvvvv',validated_data)
    #     return ConnectedShop.objects.create(**validated_data)

class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender_shop = ShopsSerializer()
    class Meta:
        model = ConnectedShop
        fields = ['sender_shop']


class ConnectionRequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedShop
        fields = ['status','sender_shop']


class ProductAddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product','quentity']


class CartSerializer(serializers.ModelSerializer):
    cart_total = serializers.SerializerMethodField()
    product = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['product','quentity','unite_price','cart_total']

    def get_cart_total(self,obj):
        return obj.product.price*obj.quentity
    

class ConfermOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = []


class ConfermOrderListSerializer(serializers.ModelSerializer):
    #products = ShopProductsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','shop_name','merchant','cart_total_price','order_date']

