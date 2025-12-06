from django.db import models

# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=200)
    bulding = models.CharField(max_length=200)
    capacity = models.IntegerField(max_length=150)
    location = models.CharField(max_length=200)
    amneties = models.CharField(max_length=200)
    contact_phone = models.Varchar(max_length=50)

    def __str__(self):
        return self().name

class Booking(models.Models):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    add_user = models.ForeignKey(add_user, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.BooleanField()

    def __str__(self):
        return f"Booking for {self.venue}"