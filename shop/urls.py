from django.urls import path
from .views import AddCategoryView, CartProductsView, ConfermOrderListView, ConfermOrderView, ConnectedShopProducts, ConnectionRequestResponseView, ConnectionRequestSendView, ConnectionRequestView, MerchantShopsView, ProductAddToCartView, SameCategoryShopsView, ShopCreateView, ShopDetailView, ShopProductAddView, ShopProductsView, ConnectedShopView, ShopRemoveView

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'ms',SMOdelViewset,basename='shop'),


urlpatterns = [

    path('addcategory',AddCategoryView.as_view(),name='add-category'),
    path('createshop',ShopCreateView.as_view(),name='shop-create'),
    path('remove/<int:pk>',ShopRemoveView.as_view(),name='remove-shop'),
    path('shops',MerchantShopsView.as_view(),name='shops'),
    path('shop/<int:pk>',ShopDetailView.as_view(),name='shop'),

    path('shop/<int:pk>/add-product',ShopProductAddView.as_view(),name='add-product'),
    path('shop/<int:pk>/products',ShopProductsView.as_view(),name='products'),

    path('shop/<int:pk>/category',SameCategoryShopsView.as_view(),name='same-category-shops'),
    
    path('shop/<int:pk>/send',ConnectionRequestSendView.as_view(),name='connection-request-send'),
    path('shop/<int:pk>/requests',ConnectionRequestView.as_view(),name='requests'),
    path('shop/<int:pk>/response',ConnectionRequestResponseView.as_view(),name='response'),
    path('shop/<int:pk>/connected',ConnectedShopView.as_view(),name='connected-shop'),
    path('shop/<int:pk>/products/<int:shop_id>',ConnectedShopProducts.as_view(),name='connected-shop-products'),

    path('shop/<int:pk>/addtocart/<int:shop_id>',ProductAddToCartView.as_view(),name='add-to-cart'),
    path('shop/<int:pk>/cart',CartProductsView.as_view(),name='cart'),
    path('shop/<int:pk>/order',ConfermOrderView.as_view(),name='order'),
    path('shop/<int:pk>/orders',ConfermOrderListView.as_view(),name='orders'),

    
]

# urlpatterns += router.urls
