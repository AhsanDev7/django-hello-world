import factory
from faker import Faker
from myapp.models import Book, Author, Publisher, Genre

fake = Faker()

class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker("company")
    location = factory.Faker("address")
    established_year = factory.Faker("year")
    website = factory.Faker("url")
    contact_email = factory.Faker("email")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    nationality = factory.Faker("country")


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    published_date = factory.Faker("date")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    stock_quantity = factory.Faker("random_int", min=1, max=100)
    description = factory.Faker("paragraph")
    cover_photo = factory.django.ImageField()
    publisher = factory.SubFactory(PublisherFactory)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.genres.add(genre)
