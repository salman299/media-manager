from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MediaAPIView

# Create a router and register our viewsets with it
router = DefaultRouter()

# The API URLs are now determined automatically by the router
urlpatterns = [
    # API endpoints
    path("search/", MediaAPIView.as_view(), name="media-list"),
    # Authentication endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
