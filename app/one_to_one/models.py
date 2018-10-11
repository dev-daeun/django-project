from django.db import models


# Place optionally can be a Restaurant.
class Place(models.Model):
    name = models.CharField(
        max_length=50,
    )
    address = models.CharField(
        max_length=80,
    )

    def __str__(self):
        return f'{self.name} the place.'


class Restaurant(models.Model):
    # place_id가 곧 기본키.
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serve_hot_dogs = models.BooleanField(
        default=False,
    )
    serve_pizza = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.place.name} the restaurant.'


class Waiter(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.name} the waiter at {self.restaurant}.'
