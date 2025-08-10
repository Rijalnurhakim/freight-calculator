from django.contrib import admin
from shipping.models import Country, Category
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.register(Country)
admin.site.register(Category)

User = get_user_model()

admin.site.register(User, UserAdmin)