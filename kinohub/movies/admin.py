from django.contrib import admin

from .models import Movie, Player, Genre, Actor, Item, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visible_on_home", "position")
    list_filter = ("is_visible_on_home",)
    ordering = ("position",)
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("title",)}
     
admin.site.register(Player)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Item)
