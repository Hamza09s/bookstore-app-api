"""
Serializers for blog APIs
"""
from rest_framework import serializers

from core.models import Book, Cart


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Book
        fields = ["id", "title", "author", "price", "quantity"]
        read_only_fields = ["id"]


class CartSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, required=False)

    class Meta:
        Model = Cart
        fields = ["id", "books", "created_at"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        books = validated_data.pop("books", [])
        cart = Cart.objects.create(**validated_data)
        self._get_or_create_books(books, cart)

    def _get_or_create_books(self, books, cart):
        """Handle getting or creating books as needed."""
        auth_user = self.context["request"].user
        for book in books:
            book_obj, created = Book.objects.get_or_create(
                user=auth_user,
                **book,
                # future proof code incase you added more attributes in future
            )
            cart.books.add(book_obj)
