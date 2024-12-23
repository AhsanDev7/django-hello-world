import pytest
from datetime import date, timedelta
from django.urls import reverse
from myapp.tests.factories import BookFactory

@pytest.mark.django_db
class TestAdminFilters:
    @pytest.fixture
    def books(self):
        """
        Set up test data for books with different published dates and prices.
        """
        today = date.today()
        last_week = today - timedelta(days=7)
        BookFactory.create_batch(3, price=10.00, published_date=date.today())
        BookFactory.create_batch(2, price=25.00, published_date=date.today() - timedelta(days=3))
        BookFactory.create_batch(1, price=55.00, published_date=date.today() - timedelta(days=10))


    def test_custom_date_filter_last_7_days(self, admin_client, books):
        """
        Test the `CustomDateFilter` for books published in the last 7 days.
        """
        url = reverse('admin:myapp_book_changelist') + "?published_date=last_7_days"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.context['cl'].queryset.count() == 5

    def test_custom_date_filter_this_year(self, admin_client, books):
        """
        Test the `CustomDateFilter` for books published this year.
        """
        url = reverse('admin:myapp_book_changelist') + "?published_date=this_year"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.context['cl'].queryset.count() == 6

    def test_custom_date_filter_today(self, admin_client, books):
        """
        Test the `CustomDateFilter` for books published today.
        """
        url = reverse('admin:myapp_book_changelist') + "?published_date=today"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.context['cl'].queryset.count() == 3

    def test_price_range_filter_cheap(self, admin_client, books):
        """
        Test the `PriceRangeFilter` for books priced under $20.
        """
        url = reverse('admin:myapp_book_changelist') + "?price_range=cheap"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.context['cl'].queryset.count() == 3

    def test_price_range_filter_moderate(self, admin_client, books):
        """
        Test the `PriceRangeFilter` for books priced between $20 and $50.
        """
        url = reverse('admin:myapp_book_changelist') + "?price_range=moderate"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.context['cl'].queryset.count() == 2

    def test_price_range_filter_expensive(self, admin_client, books):
        """
        Test the `PriceRangeFilter` for books priced above $50.
        """
        url = reverse('admin:myapp_book_changelist') + "?price_range=expensive"
        response = admin_client.get(url)
        assert response.status_code == 200
        queryset = response.context['cl'].queryset
        assert queryset.count() == 1

