from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from property.models import Property
from property.serializers import PropertySerializer
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
import logging
import redis
from datetime import timedelta
import json
from my_microservice import settings
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from property.serializers import PropertyPostSerializer

# Connect to our Redis instance
redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)
logger = logging.getLogger(__name__)


class propertyView(APIView):

    uthentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PropertySerializer(many=True)})
    def get(self, request):
        # raise ServiceUnavailable
        cached_todo_items = redis_instance.get("todo_items")
        if cached_todo_items:
            logger.warning(f"Redis: {cached_todo_items}")
            data = json.loads(cached_todo_items)
            return Response(data)
        else:
            todo_items = Property.objects.all()
            serializer = PropertySerializer(todo_items, many=True)
            redis_instance.set("todo_items", json.dumps(serializer.data), 10)
            # signals.some_task_done.send(sender='abc_task_done', task_id=123)

            return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="PropertySerializer", request_body=PropertyPostSerializer
    )
    def post(self, request):
        serializer = PropertyPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayTodosView(APIView):
    def get(self, request):
        results = Property.objects.filter(expireDate=datetime.now().date())
        serializer = PropertySerializer(results, many=True)
        return Response(serializer.data)


class NextSevenDaysTodosView(APIView):
    def get(self, request):
        today = datetime.now().date()
        results = Property.objects.filter(
            expireDate__range=(today, today + timedelta(days=6))
        )
        serializer = PropertySerializer(results, many=True)
        return Response(serializer.data)


class TodoView(APIView):
    def get(self, request, id):
        cached_todo_item = redis_instance.get(f"todo_item_{id}")
        if cached_todo_item:
            logger.warning(f"Redis: {cached_todo_item}")
            data = json.loads(cached_todo_item)
            return Response(data)
        else:
            try:
                result = Property.objects.get(id=id)
            except Property.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = PropertySerializer(result)
            redis_instance.set(f"todo_item_{id}", json.dumps(serializer.data), 100)
            return Response(serializer.data)

    def put(self, request, id):
        try:
            result = Property.objects.get(id=id)
        except Property.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PropertySerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            result = Property.objects.get(id=id)
        except Property.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # serializer = PropertySerializer(result)
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
