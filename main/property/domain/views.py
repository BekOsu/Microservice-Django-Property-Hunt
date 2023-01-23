from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
import logging
import redis
from my_microservice import settings
from rest_framework import viewsets, status
from ..models import Product, Cart, CartItem
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from ..filters import ProductFilter
from drf_yasg.utils import swagger_auto_schema
# Connect to our Redis instance
from ..serializers import (
    ProductSearchSerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer)

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)
logger = logging.getLogger(__name__)


class CustomCreateModelMixin(CreateModelMixin):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductSearchView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSearchSerializer
    queryset = Product.objects.all()
    search_fields = (
        'category', 'brand', 'min_price', 'max_price', 'min_quantity', 'max_quantity', 'created_at', 'rating')
    ordering_fields = ('name', 'category', 'brand', 'rating', 'price', 'created_at')

    @swagger_auto_schema(query_serializer=ProductSearchSerializer)
    def get(self, request, format=None):
        serializer = ProductSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = Product.objects.all()

            name = serializer.validated_data.get('name')
            if name:
                queryset = queryset.filter(name__icontains=name)

            category = serializer.validated_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            brand = serializer.validated_data.get('brand')
            if brand:
                queryset = queryset.filter(brand=brand)

            min_price = serializer.validated_data.get('min_price')
            max_price = serializer.validated_data.get('max_price')
            if min_price and max_price:
                queryset = queryset.filter(price__range=(min_price, max_price))

            min_quantity = serializer.validated_data.get('min_quantity')
            max_quantity = serializer.validated_data.get('max_quantity')
            if min_quantity and max_quantity:
                queryset = queryset.filter(quantity__range=(min_quantity, max_quantity))

            created_at = serializer.validated_data.get('created_at')
            if created_at:
                queryset = queryset.filter(created_at=created_at)

            rating = serializer.validated_data.get('rating')
            if rating:
                queryset = queryset.filter(rating=rating)

            sort_by = self.request.query_params.get('sort_by')
            if sort_by:
                if sort_by and hasattr(Product, sort_by):
                    queryset = queryset.order_by(sort_by)
                else:
                    return Response({"detail": "Invalid 'sort_by' field"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset = queryset.order_by('name')

            paginator = LimitOffsetPagination()
            results = paginator.paginate_queryset(queryset, request)

            serializer = ProductSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(CustomCreateModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(query_serializer=ProductSerializer)
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            if sort_by in ('name', 'category', 'brand', 'rating', 'price', 'quantity', 'created_at'):
                queryset = queryset.order_by(sort_by)
            else:
                return Response({"detail": "Invalid 'sort_by' field"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = queryset.order_by('name')
        return queryset


class CartViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @swagger_auto_schema(query_serializer=CartSerializer)
    def list(self, request):
        """
        Retrieve the cart and its items of the authenticated user.
        """
        user_cart = Cart.objects.filter(user=request.user)
        if user_cart.exists():
            cart_items = CartItem.objects.filter(cart=user_cart.first())
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Cart not found for user"})

    @swagger_auto_schema(query_serializer=CartSerializer)
    def create(self, request):
        """
        Add a product to the cart of the authenticated user.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"})

        user_cart = Cart.objects.filter(user=request.user)
        if user_cart.exists():
            cart = user_cart.first()
        else:
            cart = Cart.objects.create(user=request.user)

        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @swagger_auto_schema(query_serializer=CartSerializer)
    def update(self, request):
        """
        Update the quantity of a cart item for the authenticated user.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"})

        user_cart = Cart.objects.filter(user=request.user)
        if user_cart.exists():
            cart = user_cart.first()
            cart_item = CartItem.objects.filter(cart=cart, product=product)
            if cart_item.exists():
                cart_item.update(quantity=quantity)
                serializer = CartItemSerializer(cart_item.first())
                return Response(serializer.data)
            else:
                return Response({"detail": "Item not found in cart"})
        else:
            return Response({"detail": "Cart not found for user"})

    @swagger_auto_schema(query_serializer=CartSerializer)
    def destroy(self, request):
        """
        Remove a cart item for the authenticated user.
        """
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"})

        user_cart = Cart.objects.filter(user=request.user)
        if user_cart.exists():
            cart = user_cart.first()
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
                return Response({"detail": "Product removed from cart"})
            except CartItem.DoesNotExist:
                return Response({"detail": "Product not found in cart"})
        else:
            return Response({"detail": "Cart not found for user"})
