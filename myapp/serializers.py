from rest_framework import serializers
from .models import Book, Order, Genre, Author, Publisher, Review
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if instance.published_date:
            data['published_date'] = instance.published_date.strftime('%B %d, %Y')
        
        data['price'] = f"${instance.price:.2f}"
        
        if instance.publisher:
            data['publisher'] = {
                "id": instance.publisher.id,
                "name": instance.publisher.name
            }
        
        if instance.authors:
            data['publisher'] = {
                "id": instance.publisher.id,
                "name": instance.publisher.name
            }
        if instance.authors.exists():
            data['authors'] = [
                {
                    "id": author.id,
                    "name": author.first_name+" "+author.last_name
                } for author in instance.authors.all()
            ]

        return data

    def get_in_stock(self,obj):
        return obj.stock_quantity > 0

class OrderSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        many=True
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user','total_price']
 
    def create(self, validated_data):
        books = validated_data.pop('books', [])  # Extract books from the payload

        # Validate stock for each book
        for book in books:
            if book.stock_quantity < 1:
                raise serializers.ValidationError(
                    f"Insufficient stock for '{book.title}'. Only {book.stock_quantity} available."
                )
        # Calculate the total price of the order
        total_price = sum(book.price for book in books)

        order = Order.objects.create(total_price=total_price, **validated_data)

        # Decrement stock quantity for each book and save
        for book in books:
            book.stock_quantity -= 1
            book.save()

        # Associate books with the order
        order.books.set(books)
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


class BookSummarySerializer(serializers.Serializer):
    title = serializers.CharField()
    publisher = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    def get_publisher(self, obj):
        return {"id": obj.publisher.id, "name": obj.publisher.name} if obj.publisher else None

    def get_authors(self, obj):
        return [{"id": author.id, "name": author.first_name} for author in obj.authors.all()]

    def get_summary(self, obj):
        return f"{obj.title} by {', '.join(author.first_name for author in obj.authors.all())}" if obj.authors.exists() else obj.title