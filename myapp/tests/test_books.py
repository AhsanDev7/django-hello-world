import os
import pytest
from myapp.models import Book
from django.conf import settings
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import timedelta, date
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.tests.factories import BookFactory, AuthorFactory, GenreFactory, PublisherFactory, UserFactory

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_books():
    """Create books with additional context using traits"""
    return BookFactory.create_batch(5, authors=[AuthorFactory(renowned=True)], genres=[GenreFactory(fiction=True)])


@pytest.fixture
def auth_client():
    """Fixture to authenticate the client using a user factory."""
    user = UserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


def test_list_books(auth_client, create_books, api_client):
    """Test retrieving a list of books (success and failure)"""
    response = auth_client.get(reverse("book-list"))
    assert response.status_code == 200
    assert len(response.data["results"]) == len(create_books)

    response = api_client.get(reverse("book-list"))
    assert response.status_code == 401


def test_retrieve_book(auth_client, create_books, api_client):
    """Test retrieving a single book (success and failure)"""
    book = create_books[0]

    response = auth_client.get(reverse("book-detail", args=[book.id]))
    assert response.status_code == 200
    assert response.data["title"] == book.title
    assert response.data["publisher"]["name"] == book.publisher.name
    assert len(response.data["authors"]) == book.authors.count()

    response = auth_client.get(reverse("book-detail", args=[999]))
    assert response.status_code == 404


def test_create_book(auth_client, api_client):
    """Test creating a new book (success and failure)"""
    publisher = PublisherFactory()
    author = AuthorFactory()
    genre = GenreFactory()

    file_path = os.path.join(settings.BASE_DIR, 'media', 'covers', 'example.jpg')

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    with open(file_path, 'rb') as img:
        cover_photo = SimpleUploadedFile("example.jpg", img.read(), content_type="image/jpeg")

    payload = {
        "title": "New Test Book",
        "published_date": "2024-01-01",
        "price": "29.99",
        "stock_quantity": 50,
        "description": "A test book description",
        "publisher": publisher.id,
        "authors": [author.id],
        "genres": [genre.id],
        "cover_photo": cover_photo,
    }

    response = auth_client.post(reverse("book-list"), payload)
    assert response.status_code == 201
    assert Book.objects.filter(title="New Test Book").exists()

    invalid_payload = {
        "title": "",
        "published_date": "2024-01-01",
    }
    response = auth_client.post(reverse("book-list"), invalid_payload)
    assert response.status_code == 400


def test_update_book(auth_client, create_books):
    """Test updating an existing book (success and failure)"""
    book = create_books[0]
    new_title = "Updated Book Title"
    payload = {"title": new_title}

    response = auth_client.patch(reverse("book-detail", args=[book.id]), payload)
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.title == new_title

    response = auth_client.patch(reverse("book-detail", args=[999]), payload)
    assert response.status_code == 404


def test_delete_book(auth_client, create_books):
    """Test deleting a book (success and failure)"""
    book = create_books[0]

    response = auth_client.delete(reverse("book-detail", args=[book.id]))
    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()

    response = auth_client.delete(reverse("book-detail", args=[999]))
    assert response.status_code == 404

def test_filter_books_by_price(auth_client, create_books):
    """Test filtering books by price range."""
    BookFactory.create_batch(2, price=10.00)
    BookFactory.create_batch(3, price=30.00)
    BookFactory.create_batch(1, price=100.00)

    response = auth_client.get(reverse("book-list") + "?price_min=0&price_max=20")
    assert response.status_code == 200
    assert len(response.data["results"]) == 2

    response = auth_client.get(reverse("book-list") + "?price_min=20&price_max=50")
    assert response.status_code == 200
    assert len(response.data["results"]) == 3

    response = auth_client.get(reverse("book-list") + "?price_min=50&price_max=150")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1


def test_filter_books_by_published_date(auth_client, create_books):
    """Test filtering books by published date range."""
    today = date.today()
    last_week = today - timedelta(days=7)

    BookFactory.create_batch(3, published_date=today)
    BookFactory.create_batch(2, published_date=last_week)

    response = auth_client.get(reverse('book-list') + "?published_date_range=today")
    assert response.status_code == 200
    assert len(response.data["results"]) == 3

    response = auth_client.get(reverse('book-list') + "?published_date_range=last_7_days")
    print(f"response: {response}")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5

    response = auth_client.get(reverse("book-list") + "?published_date_range=this_year")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5

def test_search_books(auth_client, create_books):
    """Test searching for books by title or description."""
    BookFactory.create(title="Django for Beginners", description="Learn Django step by step")
    BookFactory.create(title="Advanced Python", description="Deep dive into Python programming")
    BookFactory.create(title="JavaScript Essentials", description="Master JavaScript basics")

    response = auth_client.get(reverse("book-list") + "?search=Django")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Django for Beginners"

    response = auth_client.get(reverse("book-list") + "?search=Python")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["description"] == "Deep dive into Python programming"


def test_pagination(auth_client):
    """Test pagination in the book list API."""
    BookFactory.create_batch(15)

    response = auth_client.get(reverse("book-list"))
    assert response.status_code == 200
    assert len(response.data["results"]) == 5
    assert response.data["count"] == 15

    response = auth_client.get(reverse("book-list") + "?page=2")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5

    response = auth_client.get(reverse("book-list") + "?page_size=10")
    assert response.status_code == 200
    assert len(response.data["results"]) == 10

def test_combined_filters(auth_client):
    """Test combining filters, search, and pagination."""

    BookFactory.create(title="Python Basics", price=10.00, published_date=date.today())
    BookFactory.create(title="Advanced Django", price=30.00, published_date=date.today() - timedelta(days=3))
    BookFactory.create(title="JavaScript Pro", price=50.00, published_date=date.today() - timedelta(days=10))

    response = auth_client.get(reverse("book-list") + "?price_min=20&search=Django&page=1&page_size=2")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Advanced Django"
