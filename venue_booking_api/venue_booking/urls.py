
from django.urls import path
from .views import (
    HealthCheck,
    VenueListCreateView,
    VenueDetailView,
    BookingListCreateView,
    BookingDetailView,
)

urlpatterns = [
    path("health/", HealthCheck.as_view(), name="health"),
    path("venues/", VenueListCreateView.as_view(), name="venue-list"),
    path("venues/<int:pk>/", VenueDetailView.as_view(), name="venue-detail"),
    path("bookings/", BookingListCreateView.as_view(), name="booking-list"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
]
