from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
import logging
import redis
from my_microservice import settings
from rest_framework import viewsets, status
from ..models import Product
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from ..filters import ProductFilter
from drf_yasg.utils import swagger_auto_schema
# Connect to our Redis instance
from ..serializers import ProductSearchSerializer, ProductSerializer

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)
logger = logging.getLogger(__name__)


class CustomCreateModelMixin(CreateModelMixin):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductSearchView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    search_fields = (
        'category', 'brand', 'min_price', 'max_price', 'min_quantity', 'max_quantity', 'created_at', 'rating')
    ordering_fields = ('name', 'category', 'brand', 'rating', 'price', 'quantity', 'created_at')

    @swagger_auto_schema(query_serializer=ProductSearchSerializer)
    def get(self, request, format=None):
        serializer = ProductSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = Product.objects.all()

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
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ProductFilter
    pagination_class = LimitOffsetPagination
    search_fields = (
        'category', 'brand', 'min_price', 'max_price', 'min_quantity', 'max_quantity', 'created_at', 'rating')
    ordering_fields = ('name', 'category', 'brand', 'rating', 'price', 'quantity', 'created_at')

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
