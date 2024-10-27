from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant') 
    search_fields = ('user__username', 'restaurant__name')  

admin.site.register(Favorite, FavoriteAdmin)
