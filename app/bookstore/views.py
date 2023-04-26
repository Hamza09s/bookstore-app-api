"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)

# mixin is additional things you can mix in the
# view to add in functionality
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.models import Book, Cart
from bookstore import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


class BookStoreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [JWTAuthentication]
    # using token authentication for our case
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        """Retrieve blogs for authenticated user."""
        queryset = self.queryset
        return queryset.order_by("-id")


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.CartSerializer
    queryset = Cart.objects.all()
    authentication_classes = [JWTAuthentication]
    # using token authentication for our case
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Cart for authenticated user."""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by("-id")

    @extend_schema(
        request=None,  # set request_body to None to hide it in Swagger
    )
    @action(detail=False, methods=["post"], url_path="check_out_cart")
    def my_cart(self, request, pk=None):
        queryset = self.queryset
        final_queryset = queryset.filter(user=self.request.user).order_by("-id")
        return Response(final_queryset.delete())
