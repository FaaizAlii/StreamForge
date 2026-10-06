from django.contrib.auth.models import User
from langchain.tools import ToolRuntime

from content.models import Movie, Show
from subscriptions.models import Subscription

from langchain.tools import tool

@tool
def get_customer_info(runtime: ToolRuntime):
    """Get information about the currently authenticated StreamForge customer."""

    user_id = runtime.context["user_id"]

    user = (
        User.objects
        .select_related("profile")
        .filter(id=user_id)
        .first()
    )

    if not user:
        return {"error": "Customer not found."}

    return {
        "username": user.username,
        "email": user.email,
        "name": user.get_full_name(),
        "city": user.profile.city if hasattr(user, "profile") else "",
    }

@tool
def get_customer_subscription(runtime: ToolRuntime):
    """Get the subscription of the currently authenticated StreamForge customer."""

    user_id = runtime.context["user_id"]

    subscription = (
        Subscription.objects
        .filter(
            user_id=user_id,
            status=Subscription.Status.ACTIVE,
        )
        .select_related("plan")
        .first()
    )

    if not subscription:
        return {
            "has_subscription": False,
            "message": "Customer does not have an active subscription.",
        }

    return {
        "has_subscription": True,
        "plan": subscription.plan.name,
        "price": float(subscription.plan.price),
        "quality": subscription.plan.max_quality,
        "status": subscription.status,
        "start_date": subscription.start_date.isoformat(),
        "end_date": subscription.end_date.isoformat(),
        "can_view_descriptions": subscription.plan.can_view_descriptions,
    }

@tool
def search_movies(query: str):
    """Search StreamForge movies by title."""

    movies = Movie.objects.filter(
        title__icontains=query
    ).prefetch_related("genres")[:10]

    return [
        {
            "id": movie.id,
            "title": movie.title,
            "release_date": str(movie.release_date),
            "age_rating": movie.age_rating,
            "genres": [genre.name for genre in movie.genres.all()],
        }
        for movie in movies
    ]


@tool
def search_shows(query: str):
    """Search StreamForge TV shows by title."""

    shows = Show.objects.filter(
        title__icontains=query
    ).prefetch_related("genres")[:10]

    return [
        {
            "id": show.id,
            "title": show.title,
            "release_date": str(show.release_date),
            "age_rating": show.age_rating,
            "genres": [genre.name for genre in show.genres.all()],
        }
        for show in shows
    ]


@tool
def get_movie_details(movie_id: int):
    """Get details about a specific StreamForge movie."""

    movie = (
        Movie.objects
        .prefetch_related("genres")
        .filter(id=movie_id)
        .first()
    )

    if not movie:
        return {"error": "Movie not found."}

    return {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "release_date": str(movie.release_date),
        "duration_minutes": movie.duration,
        "age_rating": movie.age_rating,
        "genres": [genre.name for genre in movie.genres.all()],
    }


@tool
def get_show_details(show_id: int):
    """Get details about a specific StreamForge show."""

    show = (
        Show.objects
        .prefetch_related("genres")
        .filter(id=show_id)
        .first()
    )

    if not show:
        return {"error": "Show not found."}

    return {
        "id": show.id,
        "title": show.title,
        "description": show.description,
        "release_date": str(show.release_date),
        "age_rating": show.age_rating,
        "genres": [genre.name for genre in show.genres.all()],
    }


@tool
def search_movies_by_genre(genre: str):
    """Search StreamForge movies belonging to a specific genre."""

    movies = (
        Movie.objects
        .filter(genres__name__icontains=genre)
        .prefetch_related("genres")
        .distinct()[:10]
    )

    return [
        {
            "id": movie.id,
            "title": movie.title,
            "release_date": str(movie.release_date),
            "age_rating": movie.age_rating,
            "genres": [g.name for g in movie.genres.all()],
        }
        for movie in movies
    ]


@tool
def search_shows_by_genre(genre: str):
    """Search StreamForge shows belonging to a specific genre."""

    shows = (
        Show.objects
        .filter(genres__name__icontains=genre)
        .prefetch_related("genres")
        .distinct()[:10]
    )

    return [
        {
            "id": show.id,
            "title": show.title,
            "release_date": str(show.release_date),
            "age_rating": show.age_rating,
            "genres": [g.name for g in show.genres.all()],
        }
        for show in shows
    ]

@tool
def list_movies():
    """List all movies available on StreamForge."""

    movies = (
        Movie.objects
        .prefetch_related("genres")
        .all()
    )

    return [
        {
            "id": movie.id,
            "title": movie.title,
            "release_date": str(movie.release_date),
            "age_rating": movie.age_rating,
            "genres": [genre.name for genre in movie.genres.all()],
        }
        for movie in movies
    ]


@tool
def list_shows():
    """List all TV shows available on StreamForge."""

    shows = (
        Show.objects
        .prefetch_related("genres")
        .all()
    )

    return [
        {
            "id": show.id,
            "title": show.title,
            "release_date": str(show.release_date),
            "age_rating": show.age_rating,
            "genres": [genre.name for genre in show.genres.all()],
        }
        for show in shows
    ]


@tool
def search_support_docs(query: str) -> dict:
    """
    Search the StreamForge support documentation.

    Use this tool for questions about:
    - subscription plans
    - pricing and plan limits
    - refund policies
    - billing policies
    - feature access
    - troubleshooting
    - account security
    - support procedures
    - frequently asked questions

    Do not use this tool for customer-specific information such as
    invoices, orders, subscriptions, or support tickets.
    """
    from ai.rag import retriever

    documents = retriever.invoke(query)

    if not documents:
        return {
            "found": False,
            "message": "No relevant support documentation was found.",
        }

    results = []

    for document in documents:
        results.append({
            "content": document.page_content,
            "source": document.metadata.get("source"),
            "page": document.metadata.get("page"),
        })

    return {
        "found": True,
        "results": results,
    }


TOOLS = [
    get_customer_info,
    get_movie_details,
    get_show_details,
    get_customer_subscription,
    search_movies,
    search_movies_by_genre,
    search_shows,
    search_shows_by_genre,
    list_movies,
    list_shows,
    search_support_docs,
]