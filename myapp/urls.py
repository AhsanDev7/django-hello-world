from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, OrderViewSet, GenreViewSet, AuthorViewSet, 
    PublisherViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'order', OrderViewSet)
router.register(r'genre', GenreViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'publisher', PublisherViewSet)
router.register(r'review', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
