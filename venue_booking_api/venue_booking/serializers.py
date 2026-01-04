from rest_framework import serializers
from .models import Venue, Booking
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    venue_name = serializers.CharField(
        source="venue.name",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "venue",
            "venue_name",
            "user",
            "date",
            "start_time",
            "end_time",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate(self, data):
        """
        Prevents overlapping bookings for the same venue and date.
        """
        venue = data.get("venue")
        date = data.get("date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        qs = Booking.objects.filter(
            venue=venue,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )

        # Exclude current booking when updating
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "This venue is already booked for the selected time."
            )

        return data
