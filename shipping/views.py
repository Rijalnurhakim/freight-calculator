from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from knox.models import AuthToken
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import User, Country, Category
from .serializers import RegisterSerializer, UserSerializer, CountrySerializer, CategorySerializer

from .form import RegisterForm
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
import requests
from django.conf import settings
from django.shortcuts import render

from .rajaongkir import get_rajaongkir_api

# import environ
# User = get_user_model()

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, requests, *args, **kwargs):
        serializer = self.get_serializer(data=requests.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1   ]
        })

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            token = AuthToken.objects.create(user)[1]
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Token.objects.get_or_create(user=user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
    #     username = request.POST["username"]
    #     email = request.POST["email"]
    #     password = request.POST["password"]
    #     user = User.objects.create_user(username=username, email=email, password=password)
    #     login(request, user)
    #     return redirect('/')
    # return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    countries = Country.objects.all()
    categories = Category.objects.all()
    return render(request, 'dashboard.html', {
        'countries': countries,
        'categories': categories
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')

# CRUD Views for Countries
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_country(request):
    try:
        data = json.loads(request.body)
        country = Country.objects.create(
            country_name=data['country_name'],
            country_flag=data['country_flag'],
            country_currency=data['country_currency']
        )
        return JsonResponse({
            'success': True,
            'message': 'Country created successfully',
            'country': {
                'id': country.id,
                'country_name': country.country_name,
                'country_flag': country.country_flag,
                'country_currency': country.country_currency
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def get_country(request, country_id):
    try:
        country = get_object_or_404(Country, id=country_id)
        return JsonResponse({
            'success': True,
            'country': {
                'id': country.id,
                'country_name': country.country_name,
                'country_flag': country.country_flag,
                'country_currency': country.country_currency
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_country(request, country_id):
    try:
        data = json.loads(request.body)
        country = get_object_or_404(Country, id=country_id)

        country.country_name = data['country_name']
        country.country_flag = data['country_flag']
        country.country_currency = data['country_currency']
        country.save()

        return JsonResponse({
            'success': True,
            'message': 'Country updated successfully',
            'country': {
                'id': country.id,
                'country_name': country.country_name,
                'country_flag': country.country_flag,
                'country_currency': country.country_currency
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_country(request, country_id):
    try:
        country = get_object_or_404(Country, id=country_id)
        country_name = country.country_name
        country.delete()

        return JsonResponse({
            'success': True,
            'message': f'Country "{country_name}" deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# CRUD Views for Categories
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_category(request):
    try:
        data = json.loads(request.body)
        country = get_object_or_404(Country, id=data['country'])

        category = Category.objects.create(
            country=country,
            category_title=data['category_title'],
            price_per_kilo=data['price_per_kilo']
        )

        return JsonResponse({
            'success': True,
            'message': 'Category created successfully',
            'category': {
                'id': category.id,
                'country': category.country.id,
                'country_name': category.country.country_name,
                'category_title': category.category_title,
                'price_per_kilo': category.price_per_kilo
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
def get_category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'country': category.country.id,
                'country_name': category.country.country_name,
                'category_title': category.category_title,
                'price_per_kilo': category.price_per_kilo
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_category(request, category_id):
    try:
        data = json.loads(request.body)
        category = get_object_or_404(Category, id=category_id)
        country = get_object_or_404(Country, id=data['country'])

        category.country = country
        category.category_title = data['category_title']
        category.price_per_kilo = data['price_per_kilo']
        category.save()

        return JsonResponse({
            'success': True,
            'message': 'Category updated successfully',
            'category': {
                'id': category.id,
                'country': category.country.id,
                'country_name': category.country.country_name,
                'category_title': category.category_title,
                'price_per_kilo': category.price_per_kilo
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        category_title = category.category_title
        category.delete()

        return JsonResponse({
            'success': True,
            'message': f'Category "{category_title}" deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


# API Views for Calculator
@api_view(['GET'])
def search_countries(request):
    """
    API untuk mencari negara berdasarkan nama.
    """
    search_query = request.GET.get('search', '')


    if search_query:
        countries = Country.objects.filter(country_name__icontains=search_query)
    else:
        countries = Country.objects.all()

    data = [{
        'id': country.id,
        'country_name': country.country_name,
        'country_flag': country.country_flag,
        'country_currency': country.country_currency,
    } for country in countries]

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def search_categories(request):
    """
    API untuk mencari kategori berdasarkan ID negara dan nama kategori.
    """
    country_id = request.GET.get('country_id')
    search_query = request.GET.get('search', '')

    if not country_id:
        return JsonResponse({'error': 'country_id is required'}, status=400)

    # Filter objek Category berdasarkan country_id dan category_title
    try:
        categories = Category.objects.filter(country_id=country_id)
        if search_query:
            categories = categories.filter(category_title__icontains=search_query)

        # Ubah queryset menjadi format JSON
        data = [{
            'id': category.id,
            'category_title': category.category_title,
            'price_per_kilo': category.price_per_kilo,
            'country_id': category.country_id,
            'country_name': category.country.country_name, # Mengambil nama negara
        } for category in categories]

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

@api_view(['GET'])
def get_destinations(request):
    """
    Mengambil destinasi domestik atau internasional dari RajaOngkir.
    """
    search_query = request.GET.get('search', '')
    destination_type = request.GET.get('type', 'domestic')

    if destination_type == 'international':
        endpoint = "https://rajaongkir.komerce.id/api/v1/destination/international-destination"
    else:
        endpoint = "https://rajaongkir.komerce.id/api/v1/destination/domestic-destination"

    # Selalu sertakan parameter 'search' karena API membutuhkannya
    params = {'search': search_query}

    headers = {
        "accept": "application/json",
        "key": settings.KOMERCE_API_KEY  # Mengambil API key dari settings.py
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return JsonResponse(data, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Gagal mengambil data dari RajaOngkir: {str(e)}"}, status=500)



@api_view(['POST'])
def calculate_freight(request):
    try:
        data = request.data
        category_id = data.get('category_id')
        destination_id = data.get('destination_id')
        weight = data.get('weight')

        if not all([category_id, destination_id, weight]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Invalid JSON payload: {str(e)}'}, status=400)

    try:
        category = Category.objects.get(id=category_id)
        origin_country = category.country

        # Hitung harga internasional
        international_price = float(weight) * category.price_per_kilo

        # Pastikan origin_city_id ada
        origin_city_id = origin_country.origin_city_id
        if not origin_city_id:
            return JsonResponse({'error': 'Origin city ID not configured for this country.'}, status=400)

    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid weight format'}, status=400)

    domestic_price = 0
    destination_name = f"Destination ID {destination_id} (dummy)"  # default dummy name

    try:
        rajaongkir_headers = {
            "accept": "application/json",
            "key": settings.KOMERCE_API_KEY
        }

        cost_url = "https://rajaongkir.komerce.id/api/v1/calculate/domestic-cost"
        payload_rajaongkir = {
            "origin": int(origin_city_id),
            "destination": int(destination_id),
            "weight": int(weight * 1000),  # kg → gram
            "courier": "jne"
        }

        print("Payload ke RajaOngkir:", payload_rajaongkir)
        cost_response = requests.post(cost_url, headers=rajaongkir_headers, json=payload_rajaongkir, timeout=10)
        cost_response.raise_for_status()
        cost_data = cost_response.json()

        if cost_data.get('meta', {}).get('status') == "success":
            services = cost_data.get('data', [])
            if services:
                domestic_cost_list = [s['cost'] for s in services if s['code'] == 'jne']
                if domestic_cost_list:
                    domestic_price = min(domestic_cost_list)
                else:
                    domestic_price = 50000  # fallback
            else:
                domestic_price = 50000  # fallback
        else:
            domestic_price = 50000  # fallback
    except requests.exceptions.RequestException as e:
        # Fallback kalau API error atau rate limit
        domestic_price = 50000
        print(f"[WARNING] RajaOngkir API error: {str(e)} - Using dummy domestic price")
    except Exception as e:
        domestic_price = 50000
        print(f"[WARNING] Unexpected error: {str(e)} - Using dummy domestic price")

    total_price = international_price + domestic_price

    response_data = {
        'origin': origin_country.country_name,
        'destination': destination_name,
        'category_name': category.category_title,
        'international_price': international_price,
        'domestic_price': domestic_price,
        'total_price': total_price
    }

    return JsonResponse(response_data)

def calculator_page(request):
    return render(request, 'calculator.html')

