"""
URL mappings for the bookstore app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from bookstore import views


router = DefaultRouter()
router.register("bookstore", views.BookStoreViewSet)
router.register("cart", views.CustomerViewSet)


app_name = "bookstore"

urlpatterns = [
    path("", include(router.urls)),
]
