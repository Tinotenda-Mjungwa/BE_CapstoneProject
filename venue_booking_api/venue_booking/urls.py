from django.urls import path, include
from .views import VenueListCreateView

urlpatterns = [
    path('venues/',VenueListCreateView.as_view(),name='venue-list-create'),
    

]