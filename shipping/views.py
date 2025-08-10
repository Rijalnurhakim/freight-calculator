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

# @api_view(['POST'])
# def api_login(request):
#     username = request.data.get['username']
#     password = request.data.get['password']
#     user = authenticate(username=username, password=password)
#     if user:
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
#     return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LoginAPIView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#
#         print(f"Mencoba login dengan username: {username} dan password: {password}")
#
#         user = authenticate(request, username=username, password=password)
#
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         else:
#             print("Otentikasi gagal!")
#             return Response({"error": "Kredensial tidak valid"}, status=status.HTTP_401_UNAUTHORIZED)

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