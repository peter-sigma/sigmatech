from django.contrib import admin

# Register your models here.
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'profile_picture')  # Fields to display in the list view
    search_fields = ('user__username', 'address')  # Fields to search by in the admin panel
    list_filter = ('user',)  # Filters to use in the admin panel
