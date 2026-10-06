import os
import sys
import django

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

WEB_DIR = os.path.join(PROJECT_ROOT, "web")
sys.path.insert(0, WEB_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django.setup()

from content.models import Movie, Show


POSTERS = {
    # Movies
    "The Last Signal":
        "https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg",

    "Karachi Nights":
        "https://images.pexels.com/photos/3052727/pexels-photo-3052727.jpeg",

    "Beyond Lahore":
        "https://images.pexels.com/photos/1485894/pexels-photo-1485894.jpeg",

    "The Silent Code":
        "https://images.pexels.com/photos/5380664/pexels-photo-5380664.jpeg",

    "Desert Storm":
        "https://images.pexels.com/photos/1001435/pexels-photo-1001435.jpeg",

    "The Forgotten City":
        "https://images.pexels.com/photos/161853/greece-athens-acropolis-landscape-monument-161853.jpeg",

    "Final Protocol":
        "https://images.pexels.com/photos/5380642/pexels-photo-5380642.jpeg",

    "The Long Road":
        "https://images.pexels.com/photos/210182/pexels-photo-210182.jpeg",

    "Midnight Train":
        "https://images.pexels.com/photos/302428/pexels-photo-302428.jpeg",

    "The Last Guardian":
        "https://images.pexels.com/photos/1631677/pexels-photo-1631677.jpeg",

    "Broken Promise":
        "https://images.pexels.com/photos/1025469/pexels-photo-1025469.jpeg",

    "The Deep":
        "https://images.pexels.com/photos/1108701/pexels-photo-1108701.jpeg",

    "Code Zero":
        "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg",

    "Hidden Truth":
        "https://images.pexels.com/photos/3769138/pexels-photo-3769138.jpeg",

    "Mountain Echo":
        "https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg",

    "Second Chance":
        "https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg",

    "Black Horizon":
        "https://images.pexels.com/photos/2150/sky-space-dark-galaxy.jpg",

    "The Missing File":
        "https://images.pexels.com/photos/205316/pexels-photo-205316.jpeg",

    "City of Dreams":
        "https://images.pexels.com/photos/466685/pexels-photo-466685.jpeg",

    "The Final Game":
        "https://images.pexels.com/photos/1263349/pexels-photo-1263349.jpeg",

    "Shadow Network":
        "https://images.pexels.com/photos/5380664/pexels-photo-5380664.jpeg",

    "The Visitor":
        "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg",

    "Parallel":
        "https://images.pexels.com/photos/2150/sky-space-dark-galaxy.jpg",

    "After Midnight":
        "https://images.pexels.com/photos/169198/pexels-photo-169198.jpeg",

    "The Messenger":
        "https://images.pexels.com/photos/3769138/pexels-photo-3769138.jpeg",

    "Lost Expedition":
        "https://images.pexels.com/photos/672358/pexels-photo-672358.jpeg",

    "Under the Surface":
        "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg",

    "The Crossing":
        "https://images.pexels.com/photos/417074/pexels-photo-417074.jpeg",

    "Zero Hour":
        "https://images.pexels.com/photos/713149/pexels-photo-713149.jpeg",

    "The New Beginning":
        "https://images.pexels.com/photos/1642125/pexels-photo-1642125.jpeg",


    # Shows
    "The Startup":
        "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg",

    "City Detectives":
        "https://images.pexels.com/photos/3769138/pexels-photo-3769138.jpeg",

    "The Family":
        "https://images.pexels.com/photos/1486974/pexels-photo-1486974.jpeg",

    "Code Room":
        "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg",

    "Northern Lights":
        "https://images.pexels.com/photos/1933316/pexels-photo-1933316.jpeg",

    "The Agency":
        "https://images.pexels.com/photos/5380664/pexels-photo-5380664.jpeg",

    "Hospital 24":
        "https://images.pexels.com/photos/263402/pexels-photo-263402.jpeg",

    "The Lawyers":
        "https://images.pexels.com/photos/5668473/pexels-photo-5668473.jpeg",

    "Campus Life":
        "https://images.pexels.com/photos/207692/pexels-photo-207692.jpeg",

    "The Restaurant":
        "https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg",

    "Dark Files":
        "https://images.pexels.com/photos/3769138/pexels-photo-3769138.jpeg",

    "The Journalist":
        "https://images.pexels.com/photos/5180065/pexels-photo-5180065.jpeg",

    "Family Business":
        "https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg",

    "The Interns":
        "https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg",

    "Borderline":
        "https://images.pexels.com/photos/1534057/pexels-photo-1534057.jpeg",

    "The Engineers":
        "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg",

    "Hidden Room":
        "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg",

    "The Travelers":
        "https://images.pexels.com/photos/346885/pexels-photo-346885.jpeg",

    "The Heist":
        "https://images.pexels.com/photos/394565/pexels-photo-394565.jpeg",

    "Tomorrow":
        "https://images.pexels.com/photos/2150/sky-space-dark-galaxy.jpg",
}


def update_posters():
    movie_count = 0
    show_count = 0

    for title, url in POSTERS.items():

        movie = Movie.objects.filter(title=title).first()

        if movie:
            movie.poster_url = url
            movie.save(update_fields=["poster_url"])
            movie_count += 1
            print(f"Movie: {title}")

            continue

        show = Show.objects.filter(title=title).first()

        if show:
            show.poster_url = url
            show.save(update_fields=["poster_url"])
            show_count += 1
            print(f"Show: {title}")

    print()
    print(f"Movies updated: {movie_count}")
    print(f"Shows updated:  {show_count}")


if __name__ == "__main__":
    update_posters()