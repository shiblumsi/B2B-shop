from rest_framework import permissions

from shop.models import Shop, ConnectedShop

class IsSameCategory(permissions.BasePermission):
    def has_permission(self, request, view):
        print('tyyyyyyyyyyy',view)
        shop = Shop.objects.get(id=view.kwargs.get('pk'))
        # receiver = Shop.objects.get(id=self.request.data['receiver_shop'])

        # if shop.category == receiver.category:
        #     return True
        return False
    

class IsShopMerchant(permissions.BasePermission):
    message = 'It\'s not your shop!!! Please visit your shop.'
    def has_permission(self, request, view):
        shop = Shop.objects.get(id=view.kwargs.get('pk'))
        return request.user == shop.merchant
    
class IsConnected(permissions.BasePermission):
    message = 'connected shops only!!!'
    def has_permission(self, request, view):
        
        shop1 = Shop.objects.get(id=view.kwargs.get('pk'))
        shop2 = Shop.objects.get(id=view.kwargs.get('shop_id'))
        conn = ConnectedShop.objects.filter(sender_shop=shop1,receiver_shop=shop2,status='ACCEPT')
        if conn:
            return True
        return False