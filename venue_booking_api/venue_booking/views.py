from django.shortcuts import render
from rest_framework import generics
from .models import Venue
from .serializers import VenueSerializer

# Create your views here.
class VenueCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
