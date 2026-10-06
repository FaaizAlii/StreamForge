from django.urls import path

from . import views


urlpatterns = [
    # UI
    path("", views.home, name="home"),
    path("movies/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("shows/<int:show_id>/", views.show_detail, name="show_detail"),

    # API
    path("api/movies/", views.movies_api, name="movies_api"),
    path("api/shows/", views.shows_api, name="shows_api"),
    path(
        "api/movies/<int:movie_id>/",
        views.movie_detail_api,
        name="movie_detail_api",
    ),
    path(
        "api/shows/<int:show_id>/",
        views.show_detail_api,
        name="show_detail_api",
    ),
]