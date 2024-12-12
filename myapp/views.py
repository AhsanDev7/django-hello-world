from rest_framework import viewsets
from rest_framework.response import Response
from .filters import BookFilter
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Book, Order, Genre, Author, Publisher, Review
from .serializers import BookSerializer, OrderSerializer,BookSummarySerializer, GenreSerializer, AuthorSerializer, PublisherSerializer, ReviewSerializer


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination
    search_fields = ['title', 'description']
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    # Custom action for book summary
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        books = Book.objects.all()
        serializer = BookSummarySerializer(books, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer