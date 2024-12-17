import os
import pytest
from myapp.models import Book,Publisher
from django.conf import settings
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from .factories import BookFactory, AuthorFactory, GenreFactory, PublisherFactory, UserFactory

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_books():
    """Create books with additional context using traits"""
    return BookFactory.create_batch(5, authors=[AuthorFactory(renowned=True)], genres=[GenreFactory(fiction=True)])


@pytest.fixture
def bestseller_books():
    """Create bestseller books with specific traits"""
    return BookFactory.create_batch(
        3,
        bestseller=True,
        authors=[AuthorFactory(renowned=True)],
        genres=[GenreFactory(fiction=True)],
        publisher=PublisherFactory.create(tech_publisher=True)
    )


def test_book_traits(bestseller_books):
    """Test the traits functionality"""
    for book in bestseller_books:
        assert book.stock_quantity >= 500
        assert book.price > 20.00
        assert book.publisher.name == "Tech Innovations Publishing"
        assert book.publisher.location == "San Francisco, CA"


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
    response = auth_client.get("/api/books/")
    assert response.status_code == 200
    assert len(response.data["results"]) == len(create_books)

    response = api_client.get("/api/books/")
    assert response.status_code == 401


def test_retrieve_book(auth_client, create_books, api_client):
    """Test retrieving a single book (success and failure)"""
    book = create_books[0]

    response = auth_client.get(f"/api/books/{book.id}/")
    assert response.status_code == 200
    assert response.data["title"] == book.title
    assert response.data["publisher"]["name"] == book.publisher.name
    assert len(response.data["authors"]) == book.authors.count()

    response = auth_client.get("/api/books/999/")
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

    response = auth_client.post("/api/books/", payload)
    assert response.status_code == 201
    assert Book.objects.filter(title="New Test Book").exists()

    # missing required fields
    invalid_payload = {
        "title": "",
        "published_date": "2024-01-01",
    }
    response = auth_client.post("/api/books/", invalid_payload)
    assert response.status_code == 400

def test_update_book(auth_client, create_books):
    """Test updating an existing book (success and failure)"""
    book = create_books[0]
    new_title = "Updated Book Title"
    payload = {"title": new_title}

    response = auth_client.patch(f"/api/books/{book.id}/", payload)
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.title == new_title

    response = auth_client.patch("/api/books/999/", payload)
    assert response.status_code == 404


def test_delete_book(auth_client, create_books):
    """Test deleting a book (success and failure)"""
    book = create_books[0]

    response = auth_client.delete(f"/api/books/{book.id}/")
    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()

    response = auth_client.delete("/api/books/999/")
    assert response.status_code == 404