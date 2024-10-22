from django.contrib import admin
from .models import Restaurant, Menu

class MenuInline(admin.TabularInline):
    model = Menu
    extra = 1  

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [MenuInline] 

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu)
