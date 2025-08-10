#!/usr/bin/env python
"""
Script to populate initial data for Country and Category models
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shipping.models import Country, Category

def populate_countries():
    """Populate initial country data"""
    countries_data = [
        {
            'country_name': 'China',
            'country_flag': 'https://flagcdn.com/w320/cn.png',
            'country_currency': 'CNY'
        },
        {
            'country_name': 'Thailand',
            'country_flag': 'https://flagcdn.com/w320/th.png',
            'country_currency': 'THB'
        },
        {
            'country_name': 'Singapore',
            'country_flag': 'https://flagcdn.com/w320/sg.png',
            'country_currency': 'SGD'
        },
        {
            'country_name': 'Malaysia',
            'country_flag': 'https://flagcdn.com/w320/my.png',
            'country_currency': 'MYR'
        },
        {
            'country_name': 'Vietnam',
            'country_flag': 'https://flagcdn.com/w320/vn.png',
            'country_currency': 'VND'
        }
    ]
    
    for country_data in countries_data:
        country, created = Country.objects.get_or_create(
            country_name=country_data['country_name'],
            defaults=country_data
        )
        if created:
            print(f"Created country: {country.country_name}")
        else:
            print(f"Country already exists: {country.country_name}")

def populate_categories():
    """Populate initial category data"""
    # Get countries
    china = Country.objects.get(country_name='China')
    thailand = Country.objects.get(country_name='Thailand')
    singapore = Country.objects.get(country_name='Singapore')
    malaysia = Country.objects.get(country_name='Malaysia')
    vietnam = Country.objects.get(country_name='Vietnam')
    
    categories_data = [
        # China categories
        {'country': china, 'category_title': 'Electronics', 'price_per_kilo': 250000},
        {'country': china, 'category_title': 'Chip', 'price_per_kilo': 300000},
        {'country': china, 'category_title': 'Laptop and Computer', 'price_per_kilo': 220000},
        {'country': china, 'category_title': 'Mobile Phone', 'price_per_kilo': 280000},
        
        # Thailand categories
        {'country': thailand, 'category_title': 'Garments', 'price_per_kilo': 200000},
        {'country': thailand, 'category_title': 'Food Products', 'price_per_kilo': 180000},
        {'country': thailand, 'category_title': 'Cosmetics', 'price_per_kilo': 240000},
        
        # Singapore categories
        {'country': singapore, 'category_title': 'Spare Parts', 'price_per_kilo': 210000},
        {'country': singapore, 'category_title': 'Machinery', 'price_per_kilo': 190000},
        {'country': singapore, 'category_title': 'Medical Equipment', 'price_per_kilo': 320000},
        
        # Malaysia categories
        {'country': malaysia, 'category_title': 'Palm Oil Products', 'price_per_kilo': 150000},
        {'country': malaysia, 'category_title': 'Rubber Products', 'price_per_kilo': 170000},
        
        # Vietnam categories
        {'country': vietnam, 'category_title': 'Textiles', 'price_per_kilo': 160000},
        {'country': vietnam, 'category_title': 'Coffee', 'price_per_kilo': 140000},
    ]
    
    for category_data in categories_data:
        category, created = Category.objects.get_or_create(
            country=category_data['country'],
            category_title=category_data['category_title'],
            defaults={'price_per_kilo': category_data['price_per_kilo']}
        )
        if created:
            print(f"Created category: {category.category_title} for {category.country.country_name}")
        else:
            print(f"Category already exists: {category.category_title} for {category.country.country_name}")

if __name__ == '__main__':
    print("Populating countries...")
    populate_countries()
    print("\nPopulating categories...")
    populate_categories()
    print("\nData population completed!")

