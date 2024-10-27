from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant')  # Menampilkan kolom ini di admin
    search_fields = ('user__username', 'restaurant__name')  # Menambahkan fungsi pencarian

admin.site.register(Favorite, FavoriteAdmin)
