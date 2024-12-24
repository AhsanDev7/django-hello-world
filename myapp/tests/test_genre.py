import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.models import Genre
from myapp.tests.factories import GenreFactory, UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Fixture to provide an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def auth_client():
    """Fixture to authenticate the client using a user factory."""
    user = UserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def create_genres():
    """Fixture to create genres for testing."""
    return GenreFactory.create_batch(5)


def test_list_genres(auth_client, create_genres, api_client):
    """Test retrieving a list of genres (success and failure)."""
    response = auth_client.get(reverse("genre-list"))
    assert response.status_code == 200
    assert len(response.data) == len(create_genres)

    response = api_client.get(reverse("genre-list"))
    assert response.status_code == 401


def test_retrieve_genre(auth_client, create_genres, api_client):
    """Test retrieving a single genre"""
    genre = create_genres[0]

    response = auth_client.get(reverse("genre-detail", args=[genre.id]))
    assert response.status_code == 200
    assert response.data["name"] == genre.name
    assert response.data["description"] == genre.description

    response = auth_client.get(reverse("genre-detail", args=[999]))
    assert response.status_code == 404


def test_create_genre(auth_client):
    """Test creating a genre."""
    genre_data = {"name": "New Genre", "description": "A test genre."}

    response = auth_client.post(reverse("genre-list"), genre_data)
    assert response.status_code == 201
    assert Genre.objects.filter(name=genre_data["name"]).exists()


def test_update_genre(auth_client, create_genres):
    """Test updating a genre."""
    genre = create_genres[0]
    updated_data = {"name": "Updated Genre", "description": "Updated description."}

    response = auth_client.put(reverse("genre-detail", args=[genre.id]), updated_data)
    assert response.status_code == 200
    genre.refresh_from_db()
    assert genre.name == updated_data["name"]
    assert genre.description == updated_data["description"]

def test_delete_genre(auth_client, create_genres):
    """Test deleting a genre."""
    genre = create_genres[0]

    response = auth_client.delete(reverse("genre-detail", args=[genre.id]))
    assert response.status_code == 204
    assert not Genre.objects.filter(id=genre.id).exists()
