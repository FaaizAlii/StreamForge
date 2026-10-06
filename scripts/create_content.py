import os
import sys
from datetime import datetime

import django


# ---------------------------------------------------------
# Django setup
# ---------------------------------------------------------

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, ROOT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.config.settings")

django.setup()


from content.models import Genre, Movie, Show


# =========================================================
# EDIT THIS
# =========================================================

CONTENT_DATA = {
    "type": "show",  # "movie" or "show"

    "title": "From",

    "description": (
        "From is an American horror television series that premiered on February 20, 2022, created by John Griffin. "
        "The show is set in a nightmarish town that traps its residents, "
        "who must survive terrifying nocturnal creatures while searching for a way to escape."
    ),

    "release_date": "2023-04-06",

    # Only required for movies
    # "duration": 125,

    "age_rating": "PG-16",

    "poster_url": (
        "https://theposterdb.com/api/assets/526391/view"
        "theposterdb-photo-8386440.jpeg"
    ),

    "genres": [
        "Horror",
        "Mystery",
        "Drama",
    ],
}


# =========================================================
# HELPERS
# =========================================================

def get_or_create_genres(genre_names):
    genres = []

    for name in genre_names:
        name = name.strip()

        if not name:
            continue

        genre, created = Genre.objects.get_or_create(
            name=name,
            defaults={
                "description": f"{name} content",
            },
        )

        if created:
            print(f"Created genre: {genre.name}")

        genres.append(genre)

    return genres


# =========================================================
# CREATE CONTENT
# =========================================================

def create_content():
    content_type = CONTENT_DATA["type"].strip().lower()

    if content_type not in ("movie", "show"):
        print("ERROR: type must be 'movie' or 'show'.")
        return

    title = CONTENT_DATA["title"].strip()

    if not title:
        print("ERROR: title is required.")
        return

    if not CONTENT_DATA["genres"]:
        print("ERROR: At least one genre is required.")
        return

    release_date = datetime.strptime(
        CONTENT_DATA["release_date"],
        "%Y-%m-%d",
    ).date()

    genres = get_or_create_genres(
        CONTENT_DATA["genres"]
    )

    if content_type == "movie":

        duration = CONTENT_DATA.get("duration")

        if not duration:
            print("ERROR: duration is required for movies.")
            return

        content = Movie.objects.create(
            title=title,
            description=CONTENT_DATA["description"],
            release_date=release_date,
            duration=duration,
            age_rating=CONTENT_DATA["age_rating"],
            poster_url=CONTENT_DATA.get("poster_url", ""),
        )

    else:

        content = Show.objects.create(
            title=title,
            description=CONTENT_DATA["description"],
            release_date=release_date,
            age_rating=CONTENT_DATA["age_rating"],
            poster_url=CONTENT_DATA.get("poster_url", ""),
        )

    content.genres.set(genres)

    print()
    print("=" * 50)
    print("Content created successfully")
    print("=" * 50)
    print(f"Type:     {content_type}")
    print(f"Title:    {content.title}")
    print(f"Genres:   {', '.join(g.name for g in genres)}")
    print(f"Released: {content.release_date}")

    if content_type == "movie":
        print(f"Duration: {content.duration} minutes")

    print(f"Rating:   {content.age_rating}")
    print("=" * 50)


if __name__ == "__main__":
    create_content()