from django.contrib import admin
from .models import Genre, Movie, Show

# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )

    search_fields = (
        "name",
    )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_date",
        "duration",
        "age_rating",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "age_rating",
        "genres",
    )

    filter_horizontal = (
        "genres",
    )


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_date",
        "age_rating",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "age_rating",
        "genres",
    )

    filter_horizontal = (
        "genres",
    )
