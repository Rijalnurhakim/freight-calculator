from django.core.management.base import BaseCommand
from shipping.models import Country, Category


class Command(BaseCommand):
    help = 'Load initial data for countries and categories'

    def handle(self, *args, **options):
        # Create Countries
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
                self.stdout.write(
                    self.style.SUCCESS(f'Created country: {country.country_name}')
                )

        # Create Categories
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

            # Malaysia categories
            {'country': malaysia, 'category_title': 'Palm Oil Products', 'price_per_kilo': 160000},
            {'country': malaysia, 'category_title': 'Rubber Products', 'price_per_kilo': 170000},

            # Vietnam categories
            {'country': vietnam, 'category_title': 'Textiles', 'price_per_kilo': 185000},
            {'country': vietnam, 'category_title': 'Coffee', 'price_per_kilo': 195000},
        ]

        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                country=category_data['country'],
                category_title=category_data['category_title'],
                defaults=category_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created category: {category.category_title} for {category.country.country_name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial data!')
        )
