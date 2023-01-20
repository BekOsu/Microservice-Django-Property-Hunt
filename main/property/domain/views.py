from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
import redis
from my_microservice import settings
from rest_framework import viewsets, status
from ..models import Product
from rest_framework.filters import SearchFilter, OrderingFilter
from ..filters import ProductFilter
from drf_yasg.utils import swagger_auto_schema
# Connect to our Redis instance
from ..serializers import ProductSearchSerializer, ProductSerializer

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)
logger = logging.getLogger(__name__)


# class ProductSearchView(APIView):
#     @swagger_auto_schema(query_serializer=ProductSearchSerializer)
#     def get(self, request, format=None):
#         serializer = ProductSearchSerializer(data=request.query_params)
#         if serializer.is_valid():
#             queryset = Product.objects.filter(
#                 category=serializer.validated_data['category'],
#                 brand=serializer.validated_data['brand'],
#                 price__range=(serializer.validated_data['min_price'], serializer.validated_data['max_price']),
#                 quantity__range=(serializer.validated_data['min_quantity'], serializer.validated_data['max_quantity']),
#                 created_at=serializer.validated_data['created_at']
#             )
#             serializer = ProductSerializer(queryset, many=True)
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductSearchView(APIView):
    @swagger_auto_schema(query_serializer=ProductSearchSerializer)
    def get(self, request, format=None):
        serializer = ProductSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = Product.objects.filter(
                category=serializer.validated_data['category'],
                brand=serializer.validated_data['brand'],
                rating=serializer.validated_data['rating'],
                price__range=(serializer.validated_data['min_price'], serializer.validated_data['max_price']),
                quantity__range=(serializer.validated_data['min_quantity'], serializer.validated_data['max_quantity']),
                created_at=serializer.validated_data['created_at']
            )
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ProductFilter
    search_fields = ('name', 'category', 'brand', 'rating')
