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

# from .form import RegisterForm
# from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from rest_framework import status


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Token.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
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
    search = request.GET.get('search', '')
    countries = Country.objects.filter(
        country_name__icontains=search
    )
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_categories(request):
    country_id = request.GET.get('country_id')
    search = request.GET.get('search', '')

    categories = Category.objects.filter(country_id=country_id)
    if search:
        categories = categories.filter(category_title__icontains=search)

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_destinations(request):
    search = request.GET.get('search', '')
    # Mock data for destinations - in real app, this would come from RajaOngkir
    destinations = [
        {'id': 1, 'city': 'Jakarta', 'province': 'DKI Jakarta'},
        {'id': 2, 'city': 'Surabaya', 'province': 'Jawa Timur'},
        {'id': 3, 'city': 'Bandung', 'province': 'Jawa Barat'},
        {'id': 4, 'city': 'Medan', 'province': 'Sumatera Utara'},
        {'id': 5, 'city': 'Semarang', 'province': 'Jawa Tengah'},
    ]

    if search:
        destinations = [d for d in destinations if search.lower() in d['city'].lower()]

    return Response(destinations)

@api_view(['POST'])
def calculate_freight(request):
    country_id = request.data.get('country_id')
    category_id = request.data.get('category_id')
    destination_id = request.data.get('destination_id')
    weight = request.data.get('weight', 0)

    try:
        country = Country.objects.get(id=country_id)
        category = Category.objects.get(id=category_id)

        # Calculate international price
        international_price = float(weight) * category.price_per_kilo

        # Mock domestic price - in real app, this would come from RajaOngkir
        domestic_price = 75000  # Fixed for demo

        total_price = international_price + domestic_price

        return Response({
            'origin': country.country_name,
            'destination': f'Destination City {destination_id}',
            'category_name': category.category_title,
            'international_price': international_price,
            'domestic_price': domestic_price,
            'total_price': total_price
        })

    except (Country.DoesNotExist, Category.DoesNotExist):
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)