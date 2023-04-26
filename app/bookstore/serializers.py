"""
Serializers for Bookstore APIs
"""
from rest_framework import serializers

from core.models import Book, Cart


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "price", "quantity"]
        read_only_fields = ["id"]


class CartSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "book_id",
            "quantity",
            "books",
            "created_at",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        auth_user = self.context["request"].user
        books = validated_data.pop("book_id", [])
        # if validated_data["books"]["quantity"] == 0:
        #     validated_data["books"]["quantity"] = 1
        cart, created = Cart.objects.get_or_create(user=auth_user, **validated_data)
        self._get_books(books, cart)
        return cart

    def update(self, instance, validated_data):
        books = validated_data.pop("book_id", [])
        self._get_books(books, instance)
        return instance

    def _get_books(self, book_id, cart):
        """Handle getting or creating books as needed."""
        auth_user = self.context["request"].user
        book_obj = Book.objects.filter(id=book_id).first()
        if book_obj:
            cart.books.add(book_obj)
