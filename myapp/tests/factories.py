import factory
from faker import Faker
from myapp.models import Book, Author, Publisher, Genre, OrderItem, Order
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.django import Password
fake = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = Password("password")

class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker("company")
    location = factory.Faker("address")
    established_year = factory.Faker("year")
    website = factory.Faker("url")
    contact_email = factory.Faker("email")

    class Params:
        tech_publisher = factory.Trait(
            name="Tech Innovations Publishing",
            location="San Francisco, CA",
            website="https://techinnovations.com"
        )

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    nationality = factory.Faker("country")

    class Params:
        renowned = factory.Trait(
            first_name="Stephen",
            last_name="King",
            nationality="American"
        )


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker("word")
    description = factory.Faker("sentence")

    class Params:
        fiction = factory.Trait(
            name="Fiction",
            description="A genre of imaginary stories"
        )

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    published_date = factory.Faker("date")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    stock_quantity = factory.Faker("random_int", min=1, max=100)
    description = factory.Faker("paragraph")
    cover_photo = factory.django.ImageField(filename="example.jpg")
    publisher = factory.SubFactory(PublisherFactory)

    class Params:

        with_authors = factory.Trait(
            authors=factory.RelatedFactoryList(
                AuthorFactory,
                factory_related_name="books",
                size=3
            )
        )

        with_genres = factory.Trait(
            genres=factory.RelatedFactoryList(
                GenreFactory,
                factory_related_name="book",
                size=2
            )
        )

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory('myapp.tests.factories.OrderFactory')
    book = factory.SubFactory(BookFactory)
    quantity = factory.Faker("random_int", min=1, max=5)

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total_price = factory.Faker("random_number", digits=5)
    status = factory.Faker("random_element", elements=['P', 'C', 'F', 'R'])
    
    class Params:
        completed = factory.Trait(
            status='C',
        )

    class Params:
        failed = factory.Trait(
            status='F',
        )
    class Params:
        pending = factory.Trait(
            status='P',
        )