from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from .models import *


class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer
   permission_classes = [permissions.AllowAny]