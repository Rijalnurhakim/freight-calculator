from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_flag = models.URLField()
    country_currency = models.CharField(max_length=10)
    origin_city_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name_plural = "Countries"

class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category_title = models.CharField(max_length=100)
    price_per_kilo = models.PositiveIntegerField()

    def __str__(self):
        return self.category_title

    class Meta:
        verbose_name_plural = "Categories"

# class User(AbstractUser):
#     pass
