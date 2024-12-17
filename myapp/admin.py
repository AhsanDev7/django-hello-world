from django.contrib import admin
from .models import Book, Review, Publisher, Author, Genre, BookGenre,OrderItem, Order
from django.utils.timezone import now
from .filters import CustomDateFilter, PriceRangeFilter


class ReviewInline(admin.TabularInline):
    """
    Inline display for reviews associated with a book.
    """
    model = Review
    extra = 1
    fields = ('user', 'review_text', 'rating')
    max_num = 5

class BookGenreInline(admin.TabularInline):
    """
    Inline display for genres associated with a book.
    """
    model = BookGenre
    extra = 1
    fields = ('genre', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin customization for the Book model.
    """
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(published_date__year=now().year)

    list_display = ('title', 'get_authors', 'publisher', 'published_date', 'price')
    search_fields = ('title', 'publisher__name', 'authors__first_name', 'authors__last_name')
    list_filter = (CustomDateFilter, PriceRangeFilter, 'publisher')
    inlines = [ReviewInline, BookGenreInline]

    def get_authors(self, obj):
        return ", ".join([author.first_name + " " + author.last_name for author in obj.authors.all()])
    get_authors.short_description = 'Authors'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin customization for the Review model.
    """
    list_display = ('book','user', 'review_text', 'rating', 'created_at')
    search_fields = ('book__title', 'review_text')
    list_filter = ('rating', 'created_at')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin customization for the Publisher model.
    """
    list_display = ('name', 'established_year', 'location')
    search_fields = ('name', 'location')
    list_filter = ('established_year',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin customization for the Author model.
    """
    list_display = ('first_name', 'last_name', 'nationality', 'get_books')
    search_fields = ('first_name', 'last_name', 'books__title')
    list_filter = ('nationality',)

    def get_books(self, obj):
        return ", ".join([book.title for book in obj.books.all()])
    get_books.short_description = 'Books'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin customization for the Genre model.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [BookGenreInline]


@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    """
    Admin customization for the BookGenre intermediary model.
    """
    list_display = ('books', 'genre', 'created_at')
    list_filter = ('genre', 'created_at')
    search_fields = ('book__title', 'genre__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem  # The through model
    extra = 1  # Number of empty forms displayed by default
    fields = ('book', 'quantity')  # Fields to display in the inline form

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'total_price','status','ordered_date')
    list_filter = ('user', 'ordered_date')
    search_fields = ('total_price', 'status','books')
    inlines = [OrderItemInline]  # Include the inline for OrderItem



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity')
    list_filter = ('order', 'book')
    search_fields = ('order__user__username', 'book__title')

