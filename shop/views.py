from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import generics, permissions

from django.shortcuts import get_object_or_404

from .serializers import AddCategorySerializer, CartSerializer, ConfermOrderListSerializer, ConfermOrderSerializer, ConnectedShopProductsSerializer, ConnectedShopSerializer, ConnectionRequestResponseSerializer, ConnectionRequestSerializer, ConnectionRequestSendSerializer, ProductAddToCartSerializer, SameCategoryShopsSerializer, ShopCreateSerializer, ShopDetailSerializer, ShopProductAddSerializer, ShopProductsSerializer, ShopRemoveSerializer, ShopsSerializer
from .models import Cart, CartItem, Order, Product, Shop, ConnectedShop
from .permissions import IsSameCategory, IsShopMerchant,IsConnected
from merchant.models import MerchantUser


class AddCategoryView(generics.CreateAPIView):
    serializer_class = AddCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ShopCreateView(generics.CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer


class ShopRemoveView(generics.DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopRemoveSerializer
    lookup_field = 'pk'


# class SMOdelViewset(ModelViewSet):
#     queryset = Shop.objects.all()
#     serializer_class = ShopCreateSerializer

class MerchantShopsView(generics.ListAPIView):
    serializer_class = ShopsSerializer
    def get_queryset(self):
        return Shop.objects.filter(merchant=self.request.user)


class ShopDetailView(generics.RetrieveAPIView):
    serializer_class = ShopDetailSerializer
    permission_classes = [IsShopMerchant]
    def get_queryset(self):
        return Shop.objects.filter(merchant=self.request.user)
    

class ShopProductAddView(generics.CreateAPIView):
    serializer_class = ShopProductAddSerializer
    permission_classes = [IsShopMerchant]

    def perform_create(self, serializer):
        shop_id = self.kwargs.get('pk')
        shop = get_object_or_404(Shop, pk=shop_id)
        category = shop.category
        serializer.save(shop=shop,category=category)
        return serializer
    

class ShopProductsView(generics.ListAPIView):
    serializer_class = ShopProductsSerializer
    permission_classes = [IsShopMerchant]

    def get_queryset(self):
        queryset = Product.objects.filter(shop=self.kwargs.get('pk')).filter(shop__merchant=self.request.user)
        return queryset
    

class ConnectedShopView(generics.ListAPIView):
    serializer_class = ConnectedShopSerializer
    permission_classes = [IsShopMerchant]

    def get_queryset(self):
        shops = ConnectedShop.objects.filter(sender_shop=self.kwargs.get('pk')).filter(status='ACCEPT')
        return shops


class ConnectedShopProducts(generics.ListAPIView):
    serializer_class = ConnectedShopProductsSerializer
    permission_classes = [IsConnected,IsShopMerchant]

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        queryset = Product.objects.filter(shop=shop_id)
        return queryset
    

class SameCategoryShopsView(generics.ListAPIView):
    serializer_class = SameCategoryShopsSerializer
    permission_classes = [IsShopMerchant]
    filterset_fields = ['name','merchant']

    def get_queryset(self):
        shop = get_object_or_404(Shop, pk = self.kwargs.get('pk'))
        queryset = Shop.objects.filter(category=shop.category)          #need correction
        return queryset
    
    
#Views for send connection request
class ConnectionRequestSendView(generics.CreateAPIView):
    serializer_class = ConnectionRequestSendSerializer
    permission_classes = [IsShopMerchant]

    def perform_create(self, serializer):
        sender_shop = Shop.objects.get(id=self.kwargs.get('pk'))
        receiver_shop = Shop.objects.get(id=self.request.data['receiver_shop'])
        if sender_shop.category == receiver_shop.category:
            que = ConnectedShop.objects.filter(sender_shop=receiver_shop,receiver_shop=sender_shop)
            if que:
                print('You r already connected or requested')
            else:
                serializer.save(sender_shop=sender_shop,receiver_shop=receiver_shop)
                return serializer
        else:
            print('Shop category are not same!!!')
   

#Views for Connection Requests   
class ConnectionRequestView(generics.ListAPIView):
    serializer_class = ConnectionRequestSerializer
    permission_classes = [IsShopMerchant]

    def get_queryset(self):
        c_requests = ConnectedShop.objects.filter(receiver_shop=self.kwargs.get('pk')).filter(status='PENDING')
        return c_requests
    

#View for Connection Requests Responce [Accept, Reject and also pending]
class ConnectionRequestResponseView(generics.UpdateAPIView):
    serializer_class = ConnectionRequestResponseSerializer
    permission_classes = [IsShopMerchant]
    def get_object(self):
        obj = get_object_or_404(ConnectedShop,sender_shop=self.request.data['sender_shop'],receiver_shop=self.kwargs.get('pk'))
        return obj


#Views for Add to Cart products
class ProductAddToCartView(APIView):
    permission_classes = [IsShopMerchant,IsConnected]

    def post(self,request,pk,shop_id):
        serializer = ProductAddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id=serializer.data['product'])
        shop = get_object_or_404(Shop,id=pk)
        from_shop = get_object_or_404(Shop,id=shop_id)
        if product.shop == from_shop:
            cart, _ = Cart.objects.get_or_create(shop=shop)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if created:
                cart_item.quentity = serializer.data['quentity']
                cart_item.save()
            else:
                cart_item.quentity += serializer.data['quentity']
                cart_item.save()
            return Response({'product added to cartitems'})
        return Response({'shop product not match'})

    
class CartProductsView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsShopMerchant]
    def get_queryset(self):
        shop = Shop.objects.get(id=self.kwargs.get('pk'))
        try:
            cart = Cart.objects.get(shop__id=shop.id)
            cartitems = CartItem.objects.filter(cart=cart)
            return cartitems
        except Exception as e:
            ValueError(e)
        


class ProductRemoveFromCartView(generics.CreateAPIView):
    pass


class ConfermOrderView(generics.CreateAPIView):
    serializer_class = ConfermOrderSerializer
    permission_classes = [IsShopMerchant]
    def perform_create(self, serializer):
        merchant = MerchantUser.objects.get(id=self.request.user.id)
        shop = Shop.objects.get(id=self.kwargs.get('pk'))
        cart = Cart.objects.get(shop=shop)
        items_total = [ci.total_price for ci in CartItem.objects.filter(cart=cart)]
        cart_total=sum(items_total)
        serializer.save(shop_name=shop.name,merchant=merchant,cart_total_price=cart_total)
        cart.delete()
        return serializer
    
class ConfermOrderListView(generics.ListAPIView):
    permission_classes = [IsShopMerchant]
    serializer_class = ConfermOrderListSerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop,id=self.kwargs.get('pk'))
        return Order.objects.filter(shop_name=shop.name)
