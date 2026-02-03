from django.contrib import admin

from .models import Movie, Player, Genre, Actor, Item, Category, Subtitle

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visible_on_home", "position")
    list_filter = ("is_visible_on_home",)
    ordering = ("position",)
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("title",)}

class SubtitleInline(admin.TabularInline):
    model = Subtitle
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [SubtitleInline]

admin.site.register(Player)
admin.site.register(Genre)
admin.site.register(Actor)