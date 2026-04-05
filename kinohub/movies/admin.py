from django.contrib import admin

from .models import (
    Actor,
    Category,
    Director,
    Genre,
    Item,
    Movie,
    Player,
    Review,
    Screenshot,
    Subtitle,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_visible_on_home", "position")
    list_filter = ("is_visible_on_home",)
    ordering = ("position",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["genres_in_filter"]


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["actors", "genres", "directors"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PlayerInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["movie", "user", "parent"]


class SubtitleInline(admin.TabularInline):
    model = Subtitle
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [SubtitleInline]
    autocomplete_fields = ["player"]


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = ("episode_number", "url")
    show_change_link = True


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    search_fields = ["title"]
    autocomplete_fields = ["movie"]
    list_display = ("title", "movie")
    search_fields = ("title", "movie__title")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    search_fields = ["movie__title"]
