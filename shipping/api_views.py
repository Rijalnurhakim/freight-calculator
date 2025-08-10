from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import requests
import json
from .models import Country, Category

@api_view(['GET'])
def search_countries(request):
    """
    API endpoint to search countries
    URL: /api/countries?search={}
    """
    search_query = request.GET.get('search', '')
    
    if search_query:
        countries = Country.objects.filter(
            country_name__icontains=search_query
        )
    else:
        countries = Country.objects.all()
    
    data = []
    for country in countries:
        data.append({
            'id': country.id,
            'country_name': country.country_name,
            'country_flag': country.country_flag,
            'country_currency': country.country_currency
        })
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_categories(request):
    """
    API endpoint to search categories based on country
    URL: /api/categories?country_id={}&search={}
    """
    country_id = request.GET.get('country_id')
    search_query = request.GET.get('search', '')
    
    if not country_id:
        return Response(
            {'error': 'country_id parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        country = Country.objects.get(id=country_id)
    except Country.DoesNotExist:
        return Response(
            {'error': 'Country not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    categories = Category.objects.filter(country=country)
    
    if search_query:
        categories = categories.filter(
            category_title__icontains=search_query
        )
    
    data = []
    for category in categories:
        data.append({
            'id': category.id,
            'category_title': category.category_title,
            'price_per_kilo': category.price_per_kilo,
            'country_name': category.country.country_name
        })
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_destinations(request):
    """
    API endpoint to search destination cities using Raja Ongkir API
    URL: /api/destination?search={city}
    """
    search_query = request.GET.get('search', '')
    
    if not search_query:
        return Response(
            {'error': 'search parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Raja Ongkir API configuration
    # Note: You need to get your own API key from rajaongkir.com
    RAJAONGKIR_API_KEY = "your_rajaongkir_api_key_here"  # Replace with actual API key
    RAJAONGKIR_BASE_URL = "https://api.rajaongkir.com/starter"
    
    try:
        # Get cities from Raja Ongkir API
        headers = {
            'key': RAJAONGKIR_API_KEY
        }
        
        response = requests.get(
            f"{RAJAONGKIR_BASE_URL}/city",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            cities = data.get('rajaongkir', {}).get('results', [])
            
            # Filter cities based on search query
            filtered_cities = []
            for city in cities:
                if search_query.lower() in city['city_name'].lower():
                    filtered_cities.append({
                        'id': city['city_id'],
                        'city_name': city['city_name'],
                        'province': city['province'],
                        'type': city['type']
                    })
            
            return Response(filtered_cities, status=status.HTTP_200_OK)
        else:
            # Fallback: return mock data if API fails
            mock_cities = [
                {'id': '501', 'city_name': 'Sukolilo, Surabaya', 'province': 'Jawa Timur', 'type': 'Subdistrict'},
                {'id': '444', 'city_name': 'Surabaya', 'province': 'Jawa Timur', 'type': 'City'},
                {'id': '153', 'city_name': 'Jakarta Pusat', 'province': 'DKI Jakarta', 'type': 'City'},
                {'id': '154', 'city_name': 'Jakarta Selatan', 'province': 'DKI Jakarta', 'type': 'City'},
                {'id': '155', 'city_name': 'Jakarta Timur', 'province': 'DKI Jakarta', 'type': 'City'},
            ]
            
            filtered_mock = [
                city for city in mock_cities 
                if search_query.lower() in city['city_name'].lower()
            ]
            
            return Response(filtered_mock, status=status.HTTP_200_OK)
            
    except requests.RequestException:
        # Return mock data if API is not available
        mock_cities = [
            {'id': '501', 'city_name': 'Sukolilo, Surabaya', 'province': 'Jawa Timur', 'type': 'Subdistrict'},
            {'id': '444', 'city_name': 'Surabaya', 'province': 'Jawa Timur', 'type': 'City'},
            {'id': '153', 'city_name': 'Jakarta Pusat', 'province': 'DKI Jakarta', 'type': 'City'},
        ]
        
        filtered_mock = [
            city for city in mock_cities 
            if search_query.lower() in city['city_name'].lower()
        ]
        
        return Response(filtered_mock, status=status.HTTP_200_OK)

@api_view(['POST'])
def calculate_freight(request):
    """
    API endpoint to calculate freight cost
    URL: /api/calculate
    Payload: {
        "country_id": int,
        "category_id": int,
        "destination_id": string,
        "weight": float
    }
    """
    try:
        country_id = request.data.get('country_id')
        category_id = request.data.get('category_id')
        destination_id = request.data.get('destination_id')
        weight = float(request.data.get('weight', 0))
        
        if not all([country_id, category_id, destination_id, weight]):
            return Response(
                {'error': 'All fields (country_id, category_id, destination_id, weight) are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get country and category
        try:
            country = Country.objects.get(id=country_id)
            category = Category.objects.get(id=category_id, country=country)
        except (Country.DoesNotExist, Category.DoesNotExist):
            return Response(
                {'error': 'Invalid country_id or category_id'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate international shipping price
        international_price = weight * category.price_per_kilo
        
        # Get domestic shipping price from Raja Ongkir API
        domestic_price = get_domestic_shipping_cost(destination_id, weight)
        
        # Calculate total price
        total_price = international_price + domestic_price
        
        response_data = {
            'origin': country.country_name,
            'destination': get_destination_name(destination_id),
            'category_name': category.category_title,
            'weight': weight,
            'international_price': international_price,
            'domestic_price': domestic_price,
            'total_price': total_price,
            'currency': 'IDR'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except ValueError:
        return Response(
            {'error': 'Invalid weight value'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def get_domestic_shipping_cost(destination_id, weight):
    """
    Get domestic shipping cost from Raja Ongkir API
    """
    # Raja Ongkir API configuration
    RAJAONGKIR_API_KEY = "your_rajaongkir_api_key_here"  # Replace with actual API key
    RAJAONGKIR_BASE_URL = "https://api.rajaongkir.com/starter"
    
    try:
        headers = {
            'key': RAJAONGKIR_API_KEY,
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'origin': '153',  # Jakarta Pusat as default origin
            'destination': destination_id,
            'weight': int(weight * 1000),  # Convert kg to grams
            'courier': 'jne'  # Use JNE as default courier
        }
        
        response = requests.post(
            f"{RAJAONGKIR_BASE_URL}/cost",
            headers=headers,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            costs = result.get('rajaongkir', {}).get('results', [])
            
            if costs and len(costs) > 0:
                services = costs[0].get('costs', [])
                if services:
                    # Return the first available service cost
                    return services[0]['cost'][0]['value']
        
        # Fallback: calculate mock domestic price
        return calculate_mock_domestic_price(weight)
        
    except requests.RequestException:
        # Fallback: calculate mock domestic price
        return calculate_mock_domestic_price(weight)

def calculate_mock_domestic_price(weight):
    """
    Calculate mock domestic shipping price when API is not available
    """
    base_price = 75000  # Base price for domestic shipping
    weight_multiplier = 5000  # Additional cost per kg
    return base_price + (weight * weight_multiplier)

def get_destination_name(destination_id):
    """
    Get destination name by ID (mock implementation)
    """
    # Mock destination mapping
    destinations = {
        '501': 'Sukolilo, Surabaya, Jawa Timur, 60117',
        '444': 'Surabaya, Jawa Timur',
        '153': 'Jakarta Pusat, DKI Jakarta',
        '154': 'Jakarta Selatan, DKI Jakarta',
        '155': 'Jakarta Timur, DKI Jakarta',
    }
    
    return destinations.get(destination_id, f'Destination ID: {destination_id}')

