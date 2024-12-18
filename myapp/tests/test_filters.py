import pytest
from datetime import timedelta
from django.utils import timezone
from myapp.models import Book
from .factories import BookFactory

@pytest.mark.django_db
def test_book_filters():
    recent_book = BookFactory(last_7_days=True)
    old_book = BookFactory(published_date=timezone.now() - timedelta(days=10))
    cheap_book = BookFactory(price=5)
    expensive_book = BookFactory(price=50)

    recent_books = Book.objects.filter(published_date__gte=timezone.now() - timedelta(days=7))
    
    assert recent_book in recent_books
    assert old_book not in recent_books

    cheap_books = Book.objects.filter(price__lte=10)
    assert cheap_book in cheap_books
    assert expensive_book not in cheap_books
