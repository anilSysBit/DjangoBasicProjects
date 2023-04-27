from django.http import HttpResponse

from .pagination import DefaultPagination
from .serializers import CartItemPostSerializer, CartItemSerializer, CartItemUpdateSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderItemSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateOrderSerializer
from django.db.models import Count
# Create your views here.
from .models import Cart, CartItem, Customer, Product, Order, OrderItem, Collection, ProductImage, Review
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from .permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermissions
from rest_framework.permissions import DjangoModelPermissions

class CollectionViewSet(ModelViewSet): 
    queryset = Collection.objects.annotate(
        products_count=Count('products')
    ).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Cannot Delete,This Collection is Associated to Many Products on Product Table'})

        return super().destroy(request, *args, **kwargs)


# Class Views  APIViews from rest_framework.views

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id']
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):

        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Cannot be Deleted Product is Been Ordered'})
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # if only using the queryset method then from every products the any of the reviews are available

    # so you should overwrite the get_queryset method to validated the results
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    # serializer_class = CartItemSerializer 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemPostSerializer
        if self.request.method == 'PATCH':
            return CartItemUpdateSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    



class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    permission_classes = [IsAdminUser]


    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated()])
    def me(self,request):
        (customer,created)  = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data) 
        
    @action(detail=True,permission_classes=[ViewCustomerHistoryPermissions ])
    def history(self,request,pk):
        return Response("History Permitted")

    

class OrderViewSet(ModelViewSet):

    http_method_names = ['get','post','patch','delete','head','options']
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
 

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        customer_id =Customer.objects.only('id').get(user_id=self.request.user.id)
        return  Order.objects.filter(customer_id=customer_id)
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer 

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


