from django.contrib import admin

from .models import Movie, Player, Genre, Actor, Item, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visible_on_home", "position")
    list_filter = ("is_visible_on_home",)
    ordering = ("position",)
    
admin.site.register(Movie)
admin.site.register(Player)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Item)
