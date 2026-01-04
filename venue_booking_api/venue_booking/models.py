from django.db import models
from django.conf import settings
from django.utils import timezone


class Venue(models.Model):
    name = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    amenities = models.TextField(blank=True)
    contact_phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.venue.name} booked by {self.user}"


