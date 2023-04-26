"""
Tests for book APIs.
"""
from decimal import Decimal

# import tempfile
# import os


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book, Cart
from bookstore.serializers import BookSerializer, CartSerializer

CART_URL = reverse("bookstore:cart-list")


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
        res = self.client.get(CART_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookStoreApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="test123")
        # was using get_user_model.create before
        self.client.force_authenticate(self.user)

    def test_retrieve_cart(self):
        book = create_book(user=self.user)

        res = self.client.get(CART_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_cart_with_existing_books(self):
        """Test creating a recipe with existing tag."""
        book_new = create_book(user=self.user, title="Indian")
        # payload = {
        #     "title": "Pongal",
        #     "author": "Sam",
        #     "price": Decimal("4.50"),
        #     "quantity": 1,
        # }
        cart_payload = {"book_id": 1, "quantity": 1}
        # since names match we expect the above tag to be used
        # rather a new tag be created
        res = self.client.post(CART_URL, cart_payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_check_out(self):
        """testing checking out the cart"""
        book1 = create_book(user=self.user)
        book2 = create_book(user=self.user)
        cart_payload = {"book_id": 1, "quantity": 1}

        # since names match we expect the above tag to be used
        # rather a new tag be created
        res = self.client.post(CART_URL, cart_payload, format="json")
