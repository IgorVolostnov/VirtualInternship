from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewset, PerevalAddedViewset, ImageAPIView

router = routers.DefaultRouter()
router.register(r'author', AuthorViewset)
router.register(r'pereval', PerevalAddedViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('images/', ImageAPIView.as_view(), name='images-list'),
]