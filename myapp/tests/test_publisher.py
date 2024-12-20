import pytest
from myapp.models import Publisher
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .factories import PublisherFactory, UserFactory

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_publishers():
    return PublisherFactory.create_batch(5)

@pytest.fixture
def auth_client():
    """Fixture to authenticate the client using a user factory."""
    user = UserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client

@pytest.mark.django_db
class TestPublisherAPI:

    def test_create_publisher(self, auth_client):
        """Test creating a publisher"""
        valid_payload = {
            "name": "Test Publisher",
            "location": "Test Location",
            "established_year": 2020,
        }
        url = reverse("publisher-list")
        response = auth_client.post(url, valid_payload)
        assert response.status_code == 201
        assert response.data["name"] == valid_payload["name"]

        invalid_payload = {
            "name": "",
            "location": "Test Location",
            "established_year": "invalid_year",
            "website": "not-a-valid-url",
            "contact_email": "invalid-email",
        }
        response = auth_client.post(url, invalid_payload)
        assert response.status_code == 400
        assert "name" in response.data
        assert "established_year" in response.data
        assert "website" in response.data
        assert "contact_email" in response.data

    def test_list_publishers(self, auth_client, create_publishers):
        """Test retrieving a list of publishers."""
        url = reverse("publisher-list")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == len(create_publishers)

    def test_retrieve_publisher_detail(self, auth_client):
        """Test retrieving a single publisher by ID."""
        publisher = PublisherFactory()
        url = reverse("publisher-detail", args=[publisher.id])
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data["name"] == publisher.name

    def test_update_publisher(self, auth_client):
        """Test updating a publisher"""
        publisher = PublisherFactory()
        url = reverse("publisher-detail", args=[publisher.id])

        valid_payload = {
            "name": "Updated Publisher",
            "location": "Updated Location",
            "established_year": 2022,
            "website": "https://updatedpublisher.com",
            "contact_email": "contact@updatedpublisher.com",
        }
        response = auth_client.put(url, valid_payload)
        assert response.status_code == 200
        assert response.data["name"] == valid_payload["name"]
        assert response.data["location"] == valid_payload["location"]

        invalid_payload = {
            "name": "",
            "location": "Updated Location",
            "established_year": "invalid_year",
            "website": "not-a-valid-url",
            "contact_email": "invalid-email",
        }
        response = auth_client.put(url, invalid_payload)
        assert response.status_code == 400
        assert "name" in response.data
        assert "established_year" in response.data
        assert "website" in response.data
        assert "contact_email" in response.data

    def test_delete_publisher(self, auth_client):
        """Test deleting a publisher"""
        publisher = PublisherFactory()
        url = reverse("publisher-detail", args=[publisher.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert not Publisher.objects.filter(id=publisher.id).exists()

        invalid_url = reverse("publisher-detail", args=[999999])
        response = auth_client.delete(invalid_url)
        assert response.status_code == 404
