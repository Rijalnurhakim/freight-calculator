from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Country, Category

# Country CRUD Views
@login_required
def country_list(request):
    """Display list of all countries"""
    countries = Country.objects.all()
    return render(request, 'crud/country_list.html', {'countries': countries})

@login_required
def country_create(request):
    """Create new country"""
    if request.method == 'POST':
        country_name = request.POST.get('country_name')
        country_flag = request.POST.get('country_flag')
        country_currency = request.POST.get('country_currency')
        
        if country_name and country_flag and country_currency:
            Country.objects.create(
                country_name=country_name,
                country_flag=country_flag,
                country_currency=country_currency
            )
            messages.success(request, f'Country "{country_name}" created successfully!')
            return redirect('country_list')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'crud/country_form.html', {'action': 'Create'})

@login_required
def country_update(request, pk):
    """Update existing country"""
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        country.country_name = request.POST.get('country_name')
        country.country_flag = request.POST.get('country_flag')
        country.country_currency = request.POST.get('country_currency')
        
        if country.country_name and country.country_flag and country.country_currency:
            country.save()
            messages.success(request, f'Country "{country.country_name}" updated successfully!')
            return redirect('country_list')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'crud/country_form.html', {
        'country': country, 
        'action': 'Update'
    })

@login_required
def country_delete(request, pk):
    """Delete country"""
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        country_name = country.country_name
        country.delete()
        messages.success(request, f'Country "{country_name}" deleted successfully!')
        return redirect('country_list')
    
    return render(request, 'crud/country_confirm_delete.html', {'country': country})

# Category CRUD Views
@login_required
def category_list(request):
    """Display list of all categories"""
    categories = Category.objects.select_related('country').all()
    return render(request, 'crud/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    """Create new category"""
    countries = Country.objects.all()
    
    if request.method == 'POST':
        country_id = request.POST.get('country')
        category_title = request.POST.get('category_title')
        price_per_kilo = request.POST.get('price_per_kilo')
        
        if country_id and category_title and price_per_kilo:
            try:
                country = Country.objects.get(id=country_id)
                Category.objects.create(
                    country=country,
                    category_title=category_title,
                    price_per_kilo=int(price_per_kilo)
                )
                messages.success(request, f'Category "{category_title}" created successfully!')
                return redirect('category_list')
            except (Country.DoesNotExist, ValueError):
                messages.error(request, 'Invalid data provided!')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'crud/category_form.html', {
        'countries': countries, 
        'action': 'Create'
    })

@login_required
def category_update(request, pk):
    """Update existing category"""
    category = get_object_or_404(Category, pk=pk)
    countries = Country.objects.all()
    
    if request.method == 'POST':
        country_id = request.POST.get('country')
        category.category_title = request.POST.get('category_title')
        price_per_kilo = request.POST.get('price_per_kilo')
        
        if country_id and category.category_title and price_per_kilo:
            try:
                category.country = Country.objects.get(id=country_id)
                category.price_per_kilo = int(price_per_kilo)
                category.save()
                messages.success(request, f'Category "{category.category_title}" updated successfully!')
                return redirect('category_list')
            except (Country.DoesNotExist, ValueError):
                messages.error(request, 'Invalid data provided!')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'crud/category_form.html', {
        'category': category,
        'countries': countries, 
        'action': 'Update'
    })

@login_required
def category_delete(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_title = category.category_title
        category.delete()
        messages.success(request, f'Category "{category_title}" deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'crud/category_confirm_delete.html', {'category': category})

# Dashboard View
@login_required
def dashboard(request):
    """Main dashboard view"""
    countries_count = Country.objects.count()
    categories_count = Category.objects.count()
    
    context = {
        'countries_count': countries_count,
        'categories_count': categories_count,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def calculator(request):
    """Freight calculator view"""
    return render(request, 'simple_calculator.html')

