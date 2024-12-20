import pytest
from rest_framework import status
from myapp.models import Author
from myapp.tests.factories import AuthorFactory, UserFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.urls import reverse

def api_client():
    return APIClient()

@pytest.fixture
def author():
    return AuthorFactory.create()

@pytest.fixture
def auth_client():
    """Fixture to authenticate the client using a user factory."""
    user = UserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client

@pytest.mark.django_db
class TestAuthorAPI:
    def test_create_author(self, auth_client):
        """Test creating an author successfully."""
        valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "nationality": "Canadian",
        }
        response = auth_client.post(reverse("author-list"), valid_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["first_name"] == valid_payload["first_name"]
        assert response.data["last_name"] == valid_payload["last_name"]
        assert response.data["nationality"] == valid_payload["nationality"]

    def test_create_author_invalid_data(self, auth_client):
        """Test creating an author with invalid data."""
        invalid_payload = {
            "first_name": "",
            "last_name": "Smith",
            "nationality": "British",
        }
        response = auth_client.post(reverse("author-list"), invalid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data

    def test_list_authors(self, auth_client, author):
        """Test listing all authors."""
        response = auth_client.get(reverse("author-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_retrieve_author(self, auth_client, author):
        """Test retrieving a specific author by ID."""
        response = auth_client.get(reverse("author-detail", args=[author.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == author.id
        assert response.data["first_name"] == author.first_name
        assert response.data["last_name"] == author.last_name

    def test_retrieve_author_not_found(self, auth_client):
        """Test retrieving a non-existing author."""
        response = auth_client.get(reverse("author-detail", args=[99999]))  # Non-existing ID
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_author(self, auth_client, author):
        """Test updating an existing author's details."""
        update_payload = {
            "first_name": "UpdatedName",
            "last_name": "UpdatedLastName",
            "nationality": "UpdatedCountry",
        }
        response = auth_client.put(reverse("author-detail", args=[author.id]), update_payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == update_payload["first_name"]
        assert response.data["last_name"] == update_payload["last_name"]
        assert response.data["nationality"] == update_payload["nationality"]

    def test_update_author_invalid_data(self, auth_client, author):
        """Test updating an author with invalid data."""
        invalid_payload = {
            "first_name": "",  # Invalid empty first name
            "last_name": "UpdatedLastName",
            "nationality": "UpdatedCountry",
        }
        response = auth_client.put(reverse("author-detail", args=[author.id]), invalid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data

    def test_delete_author(self, auth_client, author):
        """Test deleting an author."""
        response = auth_client.delete(reverse("author-detail", args=[author.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Try to retrieve the deleted author
        response = auth_client.get(reverse("author-detail", args=[author.id]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_author_not_found(self, auth_client):
        """Test deleting a non-existing author."""
        response = auth_client.delete(reverse("author-detail", args=[99999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND
