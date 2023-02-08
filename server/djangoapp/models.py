from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    mainOffice = models.CharField(max_length=50)

    def __str__(self):
        return 'It is a %s based company, named "%s". Description : %s' % (self.mainOffice, self.name, self.description)


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    dealerId = models.IntegerField()
    type = models.CharField(max_length=40, choices=[('SED', 'Sedan'), ('SUV', 'SUV'), ('WAG', 'Wagon')])
    year = models.DateField()

    color = models.CharField(max_length=15)
    def __str__(self):
        return 'Its a %s %s %s %s.' % (self.year, self.color, self.make.name, self.name)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.state = state
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name



# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    
    def __str__(self):
        return  'Dealer review : ' + self.review