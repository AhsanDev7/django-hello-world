import pytest
from myapp.models import Publisher, Author, Genre, Book, Review, Order, OrderItem, BookGenre
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal

pytestmark = pytest.mark.django_db

@pytest.fixture
def create_user():
    """Fixture for creating a test user."""
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def create_publisher():
    """Fixture for creating a test publisher."""
    return Publisher.objects.create(
        name="Test Publisher",
        location="Test City",
        established_year=2000,
        website="https://testpublisher.com",
        contact_email="contact@testpublisher.com",
    )

@pytest.fixture
def create_author():
    """Fixture for creating a test author."""
    return Author.objects.create(first_name="John", last_name="Doe", nationality="American")

@pytest.fixture
def create_genre():
    """Fixture for creating a test genre."""
    return Genre.objects.create(name="Fiction", description="Fictional Genre")

@pytest.fixture
def create_book(create_publisher, create_author, create_genre):
    """Fixture for creating a test book."""
    book = Book.objects.create(
        title="Test Book",
        publisher=create_publisher,
        published_date=date(2020, 1, 1),
        price=20.99,
        stock_quantity=50,
        description="A test book.",
        cover_photo="covers/test.jpg",
    )
    book.authors.add(create_author)
    book.genres.add(create_genre)
    return book

@pytest.fixture
def create_review(create_book, create_user):
    """Fixture for creating a test review."""
    return Review.objects.create(
        book=create_book,
        user=create_user,
        review_text="Great book!",
        rating=5,
    )

@pytest.fixture
def create_order(create_user, create_book):
    """Fixture for creating a test order."""
    order = Order.objects.create(user=create_user, total_price=0.00, status="P")
    OrderItem.objects.create(order=order, book=create_book, quantity=2)
    order.calculate_total_price()
    return order

# Test Publisher Model
def test_publisher_creation(create_publisher):
    """Test creation of Publisher model."""
    assert create_publisher is not None
    assert create_publisher.name == "Test Publisher"
    assert create_publisher.location == "Test City"

def test_publisher_str(create_publisher):
    """Test the __str__ method of Publisher."""
    expected_str = "Test Publisher"
    assert str(create_publisher) == expected_str

# Test Author Model
def test_author_creation(create_author):
    """Test creation of Author model."""
    assert create_author is not None
    assert create_author.first_name == "John"
    assert create_author.last_name == "Doe"

def test_author_str(create_author):
    """Test the __str__ method of Author."""
    expected_str = "John Doe"
    assert str(create_author) == expected_str

# Test Genre Model
def test_genre_creation(create_genre):
    """Test creation of Genre model."""
    assert create_genre is not None
    assert create_genre.name == "Fiction"

def test_genre_str(create_genre):
    """Test the __str__ method of Genre."""
    expected_str = "Fiction"
    assert str(create_genre) == expected_str

# Test Book Model
def test_book_creation(create_book):
    """Test creation of Book model."""
    assert create_book is not None
    assert create_book.title == "Test Book"
    assert create_book.price == 20.99
    assert create_book.stock_quantity == 50

def test_book_str(create_book):
    """Test the __str__ method of Book."""
    expected_str = "Test Book"
    assert str(create_book) == expected_str

# Test Review Model
def test_review_creation(create_review):
    """Test creation of Review model."""
    assert create_review is not None
    assert create_review.rating == 5
    assert create_review.review_text == "Great book!"

def test_review_str(create_review):
    """Test the __str__ method of Review."""
    expected_str = "Review by testuser for Test Book"
    assert str(create_review) == expected_str

# Test Order Model
def test_order_creation(create_order):
    """Test creation of Order model."""
    assert create_order is not None
    assert create_order.status == "P"
    assert create_order.total_price == Decimal('41.98')

def test_order_str(create_order):
    """Test the __str__ method of Order."""
    expected_str = f"Order #{create_order.id} by testuser"
    assert str(create_order) == expected_str

# Test OrderItem Model
def test_order_item_creation(create_order):
    """Test creation of OrderItem model."""
    order_item = create_order.items.first()
    assert order_item.quantity == 2
    assert order_item.book.title == "Test Book"

def test_order_item_str(create_order):
    """Test the __str__ method of OrderItem."""
    order_item = create_order.items.first()
    expected_str = f"Test Book (x2) in Order #{create_order.id}"
    assert str(order_item) == expected_str

# Test calculate_total_price in Order Model
def test_order_total_price(create_order):
    """Test total price calculation in Order model."""
    total_price = create_order.calculate_total_price()
    assert total_price == Decimal('41.98')  # 20.99 * 2