import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .filters import BookFilter
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from myapp.models import Book, Order, Genre, Author, Publisher, Review
from myapp.serializers import BookSerializer, OrderSerializer,BookSummarySerializer, GenreSerializer, AuthorSerializer, PublisherSerializer, ReviewSerializer

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination
    search_fields = ['title', 'description']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BookFilter

    # Custom action for book summary
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        books = Book.objects.all()
        serializer = BookSummarySerializer(books, many=True)
        return Response(serializer.data)
 
    # Custom action to search books using the Open Library API
    @action(detail=False, methods=['get'], url_path='open-library')
    def open_library(self, request):
        query = request.query_params.get("query", "")
        if not query:
            return Response(
                {"error": "Query parameter is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        api_url = "https://openlibrary.org/search.json"
        params = {
            "q": query,
            "fields": "key,title,author_name,editions,description",
        }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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