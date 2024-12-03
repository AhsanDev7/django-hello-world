from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Publisher(models.Model):
    """
    One-to-Many relationship with Book.
    """
    name = models.CharField(max_length=100, unique=True)
    location= models.CharField(max_length=200)
    established_year = models.PositiveIntegerField()
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)


    def __str__(self):
        return self.name

class Author(models.Model):
    """
    Many-to-Many relationship with Book.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    """
    a genre that can be assigned to multiple books. Many-to-Many relationship.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title= models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name='books')  # Many-to-Many
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')  # One-to-Many
    genres = models.ManyToManyField(Genre, through='BookGenre', related_name='books')  # Through table for Many-to-Many
    published_date= models.DateField()
    price= models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(max_length=200)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"Review by {self.user.username} for {self.book.title}"

class BookGenre(models.Model):
    """
    Relational table for Book and Genre.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.genre.name}"

class Order(models.Model):
    """
    Order model to track customer orders and link to a user.
    """
    ORDER_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders') 
    books = models.ManyToManyField(Book, through='OrderItem', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default='P')
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    """
    Relational table for Order and Book.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} (x{self.quantity}) in Order #{self.order.id}"