from django.contrib import admin

from .models import Movie, Player, Genre, Actor, Item, Category

admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Player)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Item)
