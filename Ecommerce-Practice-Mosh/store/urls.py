from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_nested import routers


router = DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet,basename='orders')



# using nested routers (pip install drf-nested-routers)

products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
products_router.register('images',views.ProductImageViewSet,basename='product-images')
cart_item_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_item_router.register('items',views.CartItemViewSet,basename='cart-items')
order_item_router = routers.NestedDefaultRouter(router,'orders',lookup='order')
order_item_router.register('items',views.OrderItemViewSet,basename='order-items')


urlpatterns = router.urls + products_router.urls+cart_item_router.urls + order_item_router.urls

# urlpatterns = [
#     path('',include(router.urls))
# ]


