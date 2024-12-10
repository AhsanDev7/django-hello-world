from rest_framework import serializers
from .models import Book, Order, Genre, Author, Publisher, Review
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        books = validated_data.pop('books', [])  # Extract the books list from payload
        order = Order.objects.create(**validated_data)  # Create the order without books ids
        order.books.set(books)  # Associate books ids with the order
        return order

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'