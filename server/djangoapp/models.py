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


# <HINT> Create a plain Python class `DealerReview` to hold review data
