from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Movie, Show


# =========================
# HTML Views
# =========================

@login_required
def home(request):
    movies = Movie.objects.prefetch_related("genres").all()
    shows = Show.objects.prefetch_related("genres").all()

    return render(
        request,
        "content/home.html",
        {
            "movies": movies,
            "shows": shows,
        },
    )

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres"),
        id=movie_id,
    )

    can_view_description = False

    if request.user.is_authenticated:
        subscription = (
            request.user.subscriptions
            .filter(status="active")
            .select_related("plan")
            .first()
        )

        if subscription:
            can_view_description = subscription.plan.can_view_descriptions

    return render(
        request,
        "content/movie_detail.html",
        {
            "movie": movie,
            "can_view_description": can_view_description,
        },
    )

@login_required
def show_detail(request, show_id):
    show = get_object_or_404(
        Show.objects.prefetch_related("genres"),
        id=show_id,
    )

    can_view_description = False

    if request.user.is_authenticated:
        subscription = (
            request.user.subscriptions
            .filter(status="active")
            .select_related("plan")
            .first()
        )

        if subscription:
            can_view_description = subscription.plan.can_view_descriptions

    return render(
        request,
        "content/show_detail.html",
        {
            "show": show,
            "can_view_description": can_view_description,
        },
    )

# =========================
# API Views
# =========================

@login_required
def movies_api(request):
    movies = Movie.objects.prefetch_related("genres").all()

    data = [
        {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_date": movie.release_date,
            "duration": movie.duration,
            "age_rating": movie.age_rating,
            "genres": [
                genre.name for genre in movie.genres.all()
            ],
        }
        for movie in movies
    ]

    return JsonResponse(data, safe=False)

@login_required
def shows_api(request):
    shows = Show.objects.prefetch_related("genres").all()

    data = [
        {
            "id": show.id,
            "title": show.title,
            "description": show.description,
            "release_date": show.release_date,
            "age_rating": show.age_rating,
            "genres": [
                genre.name for genre in show.genres.all()
            ],
        }
        for show in shows
    ]

    return JsonResponse(data, safe=False)

@login_required
def movie_detail_api(request, movie_id):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres"),
        id=movie_id,
    )

    data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "release_date": movie.release_date,
        "duration": movie.duration,
        "age_rating": movie.age_rating,
        "genres": [
            genre.name for genre in movie.genres.all()
        ],
    }

    return JsonResponse(data)

@login_required
def show_detail_api(request, show_id):
    show = get_object_or_404(
        Show.objects.prefetch_related("genres"),
        id=show_id,
    )

    data = {
        "id": show.id,
        "title": show.title,
        "description": show.description,
        "release_date": show.release_date,
        "age_rating": show.age_rating,
        "genres": [
            genre.name for genre in show.genres.all()
        ],
    }

    return JsonResponse(data)
