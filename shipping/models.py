from django.db import models

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_flag = models.URLField()
    country_currency = models.CharField(max_length=10)

    def __str__(self):
        return self.country_name

class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category_title = models.CharField(max_length=100)
    price_per_kilo = models.PositiveIntegerField()

    def __str__(self):
        return self.category_title
