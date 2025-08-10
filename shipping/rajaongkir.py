import requests
import json
from django.conf import settings


class RajaOngkirAPI:
    """
    RajaOngkir API integration for domestic shipping cost calculation
    """

    def __init__(self):
        # You need to get API key from https://rajaongkir.com/
        # For demo purposes, we'll use a placeholder
        self.api_key = getattr(settings, 'RAJAONGKIR_API_KEY', 'demo_key')
        self.base_url = 'https://api.rajaongkir.com/starter'
        self.headers = {
            'key': self.api_key,
            'content-type': 'application/x-www-form-urlencoded'
        }

    def get_provinces(self):
        """
        Get all provinces in Indonesia
        """
        try:
            url = f"{self.base_url}/province"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                if data['rajaongkir']['status']['code'] == 200:
                    return {
                        'success': True,
                        'data': data['rajaongkir']['results']
                    }

            return {
                'success': False,
                'message': 'Failed to fetch provinces'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def get_cities(self, province_id=None):
        """
        Get cities by province ID or all cities
        """
        try:
            url = f"{self.base_url}/city"
            params = {}
            if province_id:
                params['province'] = province_id

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                data = response.json()
                if data['rajaongkir']['status']['code'] == 200:
                    return {
                        'success': True,
                        'data': data['rajaongkir']['results']
                    }

            return {
                'success': False,
                'message': 'Failed to fetch cities'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def search_cities(self, search_term):
        """
        Search cities by name
        """
        try:
            # Get all cities first
            cities_result = self.get_cities()

            if not cities_result['success']:
                return cities_result

            # Filter cities by search term
            cities = cities_result['data']
            filtered_cities = []

            search_term = search_term.lower()
            for city in cities:
                city_name = city['city_name'].lower()
                province_name = city['province'].lower()

                if (search_term in city_name or
                        search_term in province_name or
                        search_term in f"{city_name}, {province_name}"):
                    filtered_cities.append({
                        'city_id': city['city_id'],
                        'city_name': city['city_name'],
                        'province': city['province'],
                        'type': city['type'],
                        'postal_code': city['postal_code']
                    })

            return {
                'success': True,
                'data': filtered_cities[:10]  # Limit to 10 results
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def calculate_shipping_cost(self, origin_city_id, destination_city_id, weight, courier='jne'):
        """
        Calculate shipping cost between two cities

        Args:
            origin_city_id: Origin city ID
            destination_city_id: Destination city ID
            weight: Weight in grams
            courier: Courier service (jne, pos, tiki)
        """
        try:
            url = f"{self.base_url}/cost"

            data = {
                'origin': origin_city_id,
                'destination': destination_city_id,
                'weight': weight,
                'courier': courier
            }

            response = requests.post(url, headers=self.headers, data=data)

            if response.status_code == 200:
                result = response.json()
                if result['rajaongkir']['status']['code'] == 200:
                    costs = result['rajaongkir']['results'][0]['costs']

                    # Get the cheapest option
                    if costs:
                        cheapest = min(costs, key=lambda x: x['cost'][0]['value'])
                        return {
                            'success': True,
                            'data': {
                                'service': cheapest['service'],
                                'description': cheapest['description'],
                                'cost': cheapest['cost'][0]['value'],
                                'etd': cheapest['cost'][0]['etd'],
                                'courier': courier.upper()
                            }
                        }

            return {
                'success': False,
                'message': 'Failed to calculate shipping cost'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


# Demo data for when RajaOngkir API is not available
class DemoRajaOngkirAPI:
    """
    Demo implementation for testing without real API key
    """

    def __init__(self):
        self.demo_cities = [
            {
                'city_id': '153',
                'city_name': 'Jakarta Pusat',
                'province': 'DKI Jakarta',
                'type': 'Kota',
                'postal_code': '10540'
            },
            {
                'city_id': '154',
                'city_name': 'Jakarta Selatan',
                'province': 'DKI Jakarta',
                'type': 'Kota',
                'postal_code': '12230'
            },
            {
                'city_id': '155',
                'city_name': 'Jakarta Timur',
                'province': 'DKI Jakarta',
                'type': 'Kota',
                'postal_code': '13330'
            },
            {
                'city_id': '156',
                'city_name': 'Jakarta Utara',
                'province': 'DKI Jakarta',
                'type': 'Kota',
                'postal_code': '14140'
            },
            {
                'city_id': '157',
                'city_name': 'Jakarta Barat',
                'province': 'DKI Jakarta',
                'type': 'Kota',
                'postal_code': '11220'
            },
            {
                'city_id': '444',
                'city_name': 'Surabaya',
                'province': 'Jawa Timur',
                'type': 'Kota',
                'postal_code': '60119'
            },
            {
                'city_id': '17',
                'city_name': 'Bandung',
                'province': 'Jawa Barat',
                'type': 'Kota',
                'postal_code': '40111'
            },
            {
                'city_id': '501',
                'city_name': 'Yogyakarta',
                'province': 'DI Yogyakarta',
                'type': 'Kota',
                'postal_code': '55111'
            },
            {
                'city_id': '399',
                'city_name': 'Semarang',
                'province': 'Jawa Tengah',
                'type': 'Kota',
                'postal_code': '50112'
            },
            {
                'city_id': '23',
                'city_name': 'Bekasi',
                'province': 'Jawa Barat',
                'type': 'Kota',
                'postal_code': '17837'
            }
        ]

    def search_cities(self, search_term):
        """
        Search cities from demo data
        """
        try:
            search_term = search_term.lower()
            filtered_cities = []

            for city in self.demo_cities:
                city_name = city['city_name'].lower()
                province_name = city['province'].lower()

                if (search_term in city_name or
                        search_term in province_name or
                        search_term in f"{city_name}, {province_name}"):
                    filtered_cities.append(city)

            return {
                'success': True,
                'data': filtered_cities
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }

    def calculate_shipping_cost(self, origin_city_id, destination_city_id, weight, courier='jne'):
        """
        Calculate demo shipping cost
        """
        try:
            # Demo calculation based on weight and distance
            base_cost = 9000  # Base cost in IDR
            weight_cost = (weight / 1000) * 2000  # Cost per kg

            # Add some variation based on city IDs
            distance_factor = abs(int(origin_city_id) - int(destination_city_id)) / 100
            distance_cost = distance_factor * 1000

            total_cost = int(base_cost + weight_cost + distance_cost)

            return {
                'success': True,
                'data': {
                    'service': 'REG',
                    'description': 'Layanan Reguler',
                    'cost': total_cost,
                    'etd': '2-3',
                    'courier': courier.upper()
                }
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }


# Factory function to get the appropriate API instance
def get_rajaongkir_api():
    """
    Get RajaOngkir API instance (real or demo)
    """
    api_key = getattr(settings, 'RAJAONGKIR_API_KEY', None)

    if api_key and api_key != 'demo_key':
        return RajaOngkirAPI()
    else:
        return DemoRajaOngkirAPI()