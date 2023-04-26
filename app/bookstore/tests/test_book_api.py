"""
Tests for book APIs.
"""
from decimal import Decimal

# import tempfile
# import os


from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book, Cart
from bookstore.serializers import BookSerializer

BOOKS_URL = reverse("bookstore:book-list")


def specific_url(book_id):
    """Create and return a book URL."""
    return reverse("bookstore:book-detail", args=[book_id])


def create_book(user, **params):
    """Create and return a sample book."""
    defaults = {
        "title": "Sample book title",
        "author": "Sample author name",
        "price": Decimal("5.25"),
        "quantity": 1,
    }
    defaults.update(params)
    book = Book.objects.create(user=user, **defaults)
    return book


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicBookStoreAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookStoreApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="secret"
        )
        # c = Client()
        # c.login(username="superuser", password="secret")
        # was using get_user_model.create before
        self.client.force_authenticate(self.user)

    def test_retrieve_books(self):
        """Test retrieving a list of books"""
        create_book(user=self.user)
        create_book(user=self.user)

        res = self.client.get(BOOKS_URL)

        books = Book.objects.all().order_by("-id")
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book(self):
        """Test creating a book."""

        payload = {
            "title": "The randoms",
            "author": "John Smith",
            "price": Decimal("5.25"),
            "quantity": 3,
        }
        res = self.client.post(BOOKS_URL, payload)
        # will post book through this endpoint
        # test creating a book through the api
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # book = Book.objects.get(id=res.data["id"])
        # # retrieving book that should be created now
        # for k, v in payload.items():
        #     self.assertEqual(getattr(book, k), v)
        # self.assertEqual(book.user, self.user)

    def test_retrieve_book(self):
        user1 = create_user(email="other@example.com", password="test123")
        book1 = create_book(user=self.user)
        book2 = create_book(user=self.user)
        url = specific_url(book1.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book = create_book(user=self.user)

        url = specific_url(book.id)
        res = self.client.get(url)

        serializer = BookSerializer(book)
        self.assertEqual(res.data, serializer.data)

    # def test_partial_update(self):
    #     """Test partial update of a book."""
    #     new_price = 5
    #     book = create_book(user=self.user, price=new_price)

    #     payload = {"title": "New Book title"}
    #     url = specific_url(book.id)
    #     res = self.client.patch(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     book.refresh_from_db()
    #     # by default db is not automatically refreshed
    #     self.assertEqual(book.title, payload["title"])
    #     self.assertEqual(book.price, new_price)
    #     self.assertEqual(book.user, self.user)

    # def test_full_update(self):
    #     """Test full update of book."""
    #     book = create_book(
    #         user=self.user,
    #         title="The new randoms",
    #         author="John Smith Cassidy",
    #         price=Decimal("4.0"),
    #         quantity=5,
    #     )

    #     payload = {
    #         "title": "The  Updated randoms",
    #         "author": "John Smith Updated",
    #         "price": Decimal("6.0"),
    #         "quantity": 8,
    #     }
    #     url = specific_url(book.id)
    #     res = self.client.put(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     book.refresh_from_db()
    #     for k, v in payload.items():
    #         self.assertEqual(getattr(book, k), v)
    #     self.assertEqual(book.user, self.user)

    # def test_retrieve_books_from_cart(self):
    #     book = create_book(user=self.user)
