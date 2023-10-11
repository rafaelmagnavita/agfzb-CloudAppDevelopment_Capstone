from django.db import models
from django import forms
from django.utils.timezone import now


# Create your models here.


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return f"{self.name} {self.description}"

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES)
    year = models.DateField()
    def __str__(self):
        return f"{self.year} {self.car_make.name} {self.name}"


class CarDealer:

    def __init__(self, _id, _rev, id, city, state, st, address, zip, lat, long, full_name, short_name):
        # Dealer id
        self._id = _id
        # Dealer rev
        self._rev = _rev
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer state
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer Full Name
        self.full_name = full_name
        # Dealer short name
        self.short_name = short_name


    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review id: " + self.id

from models import DealerReview
class DealerReviewForm(forms.ModelForm):
    class Meta:
        model = DealerReview
        fields = ['purchase', 'review', 'purchase_date', 'car_model']