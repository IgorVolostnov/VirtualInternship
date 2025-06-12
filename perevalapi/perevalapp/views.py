from drf_yasg.utils import swagger_auto_schema
from markdown import Markdown
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser


@swagger_auto_schema(format=Markdown)
class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer
   permission_classes = [AllowAny]


@swagger_auto_schema(format=Markdown)
class PerevalAddedViewset(viewsets.ModelViewSet):
   queryset = PerevalAdded.objects.all()
   serializer_class = PerevalAddedSerializer
   permission_classes = [AllowAny]


@swagger_auto_schema(format=Markdown)
class ImageAPIView(APIView):
   parser_classes = (MultiPartParser, FormParser,)

   @permission_classes([AllowAny])
   def get(self, request):
      images = PerevalImage.objects.all()
      serializer = ImageSerializer(images, many=True)
      return Response(serializer.data)

   @permission_classes([AllowAny])
   def post(self, request):
      serializer = ImageSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
