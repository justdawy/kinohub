from django.contrib import admin

from .models import Actor, Category, Genre, Item, Movie, Player, Subtitle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visible_on_home", "position")
    list_filter = ("is_visible_on_home",)
    ordering = ("position",)
    prepopulated_fields = {"slug": ("name",)}


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    autocomplete_fields = ["actors", "genres"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PlayerInline]


class SubtitleInline(admin.TabularInline):
    model = Subtitle
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [SubtitleInline]


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [ItemInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ["name"]
