from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import Venue, Booking
from .serializers import VenueSerializer, BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404


class HealthCheck(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "The API is running"})
    

class RegisterView(APIView):
    permission_classes = []  # Anyone can register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user": {"username": user.username, "email": user.email}},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=200)

        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticated]


class VenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class ApproveBookingView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = "approved"
        booking.save()

        return Response(
            {"message": "Booking approved"},
            status=status.HTTP_200_OK
        )


class RejectBookingView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = "rejected"
        booking.save()

        return Response(
            {"message": "Booking rejected"},
            status=status.HTTP_200_OK
        )
