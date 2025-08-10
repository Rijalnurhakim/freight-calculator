from django.urls import path
from knox import views as knox_views
from . import views
# from .views import LoginAPIView
# from . import api_views
# from . import crud_views

# from shipping.views import RegisterAPI, UserAPI, register_view, login_view, logout_view

urlpatterns = [
    # API Authentication
    path('api/register/', views.RegisterAPI.as_view(), name='api_register'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='api_logout'),
    path('api/user/', views.UserAPI.as_view(), name='api_user'),

    # API Calculator Endpoints
    path('api/countries/', views.search_countries, name='api_countries'),
    path('api/categories/', views.search_categories, name='api_categories'),
    path('api/destinations/', views.search_destinations, name='api_destinations'),
    path('api/calculate/', views.calculate_freight, name='api_calculate'),

    # Dashboard Views
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Authentication URLs
    # path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/user/', UserAPI.as_view(), name='user'),
    # path('api/login/', LoginAPIView.as_view(), name='api_login'),

    # Web URLs
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),

    # Dashboard
    # path('', crud_views.dashboard, name='dashboard'),
    # path('calculator/', crud_views.calculator, name='calculator'),

    # Country CRUD URLs
    # path('countries/', crud_views.country_list, name='country_list'),
    # path('countries/create/', crud_views.country_create, name='country_create'),
    # path('countries/<int:pk>/update/', crud_views.country_update, name='country_update'),
    # path('countries/<int:pk>/delete/', crud_views.country_delete, name='country_delete'),

    # Category CRUD URLs
    # path('categories/', crud_views.category_list, name='category_list'),
    # path('categories/create/', crud_views.category_create, name='category_create'),
    # path('categories/<int:pk>/update/', crud_views.category_update, name='category_update'),
    # path('categories/<int:pk>/delete/', crud_views.category_delete, name='category_delete'),

    # Freight Calculator API URLs
    # path('api/countries/', api_views.search_countries, name='api_countries'),
    # path('api/categories/', api_views.search_categories, name='api_categories'),
    # path('api/destination/', api_views.search_destinations, name='api_destinations'),
    # path('api/calculate/', api_views.calculate_freight, name='api_calculate'),
]

