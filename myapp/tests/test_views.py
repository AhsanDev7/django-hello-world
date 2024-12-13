import pytest
from rest_framework.test import APIClient
from myapp.models import Book
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .factories import BookFactory, AuthorFactory, GenreFactory, PublisherFactory

import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_books():
    author = AuthorFactory()
    genre = GenreFactory()
    books = BookFactory.create_batch(5, authors=[author], genres=[genre])
    return books



@pytest.fixture
def user():
    """Fixture to create a user for authentication."""
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def auth_client(user):
    """Fixture to authenticate the client using JWT."""
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


def test_list_books(auth_client, create_books):
    """Test retrieving a list of books"""
    response = auth_client.get("/api/books/")
    assert response.status_code == 200
    assert len(response.data["results"]) == len(create_books)


def test_retrieve_book(auth_client, create_books):
    """Test retrieving a single book"""
    book = create_books[0]
    response = auth_client.get(f"/api/books/{book.id}/")
    assert response.status_code == 200
    assert response.data["title"] == book.title
    assert response.data["publisher"]["name"] == book.publisher.name
    assert len(response.data["authors"]) == book.authors.count()


def test_create_book(auth_client):
    """Test creating a new book"""
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


def test_update_book(auth_client, create_books):
    """Test updating an existing book"""
    book = create_books[0]
    new_title = "Updated Book Title"
    payload = {"title": new_title}
    response = auth_client.patch(f"/api/books/{book.id}/", payload)
    assert response.status_code == 200
    book.refresh_from_db()
    assert book.title == new_title


def test_delete_book(auth_client, create_books):
    """Test deleting a book"""
    book = create_books[0]
    response = auth_client.delete(f"/api/books/{book.id}/")
    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()
