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

    # CRUD URLs for Countries
    path('countries/create/', views.create_country, name='create_country'),
    path('countries/<int:country_id>/', views.get_country, name='get_country'),
    path('countries/<int:country_id>/update/', views.update_country, name='update_country'),
    path('countries/<int:country_id>/delete/', views.delete_country, name='delete_country'),

    # CRUD URLs for Categories
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/', views.get_category, name='get_category'),
    path('categories/<int:category_id>/update/', views.update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    # Authentication URLs
    # path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/user/', UserAPI.as_view(), name='user'),
    # path('api/login/', LoginAPIView.as_view(), name='api_login'),

    # Web URLs
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),

]

