import pytest
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APIClient
from myapp.models import Order, Book
from rest_framework_simplejwt.tokens import RefreshToken
from myapp.tests.factories import OrderFactory, UserFactory, BookFactory
from django.urls import reverse

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def book():
    return BookFactory()

@pytest.fixture
def order(user, book):
    order = OrderFactory(user=user)
    order.books.add(book)
    return order

@pytest.fixture
def auth_client():
    """Fixture to authenticate the client using a user factory."""
    user = UserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client

@pytest.mark.django_db
class TestOrderAPI:
    
    def test_create_order(self, auth_client, book):
        """Test creating an order with valid data."""
        valid_payload = {
            "books": [book.id],
            "status": "P",
        }
        url = reverse("order-list")
        response = auth_client.post(url, valid_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert Decimal(response.data["total_price"]) == book.price

    def test_list_orders(self, auth_client, order):
        """Test listing orders."""
        url = reverse("order-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert response.data["results"][0]["id"] == order.id

    def test_retrieve_order(self, auth_client, order):
        """Test retrieving a specific order."""
        url = reverse("order-detail", args=[order.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == order.id
        assert response.data["user"] == order.user.id

    def test_update_order(self, auth_client, order):
        """Test updating an order."""
        updated_payload = {
            "status": "C",
        }
        url = reverse("order-detail", args=[order.id])
        response = auth_client.put(url, updated_payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "C"

    def test_delete_order(self, auth_client, order):
        """Test deleting an order."""
        url = reverse("order-detail", args=[order.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(id=order.id).exists()
