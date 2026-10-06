import os
import random
import sys
from datetime import timedelta
from decimal import Decimal

import django
from django.utils import timezone


# ---------------------------------------------------------
# Django setup
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from django.contrib.auth.models import User

from accounts.models import Profile
from content.models import Genre, Movie, Show
from subscriptions.models import Plan, Subscription, Payment


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

NUM_USERS = 500

PASSWORD = "Test12345!"

random.seed(42)


# ---------------------------------------------------------
# Pakistani data
# ---------------------------------------------------------

FIRST_NAMES = [
    "Muhammad",
    "Ahmed",
    "Ali",
    "Hassan",
    "Hussain",
    "Hamza",
    "Usman",
    "Bilal",
    "Saad",
    "Talha",
    "Zain",
    "Ahsan",
    "Omar",
    "Abdullah",
    "Abdul Rehman",
    "Abdul Basit",
    "Abdul Hadi",
    "Fahad",
    "Farhan",
    "Imran",
    "Kamran",
    "Salman",
    "Danish",
    "Waleed",
    "Shahzaib",
    "Rayan",
    "Maham",
    "Sadaf",
    "Ayesha",
    "Fatima",
    "Zainab",
    "Hira",
    "Iqra",
    "Laiba",
    "Maryam",
    "Areeba",
    "Alina",
    "Anaya",
    "Eman",
    "Hania",
    "Minal",
    "Mehwish",
    "Sana",
    "Mahnoor",
    "Kinza",
    "Aiman",
    "Amna",
    "Komal",
    "Rabia",
    "Sidra",
]

LAST_NAMES = [
    "Khan",
    "Ahmed",
    "Ali",
    "Malik",
    "Sheikh",
    "Butt",
    "Chaudhry",
    "Chowdhury",
    "Raza",
    "Hussain",
    "Iqbal",
    "Javed",
    "Siddiqui",
    "Qureshi",
    "Farooq",
    "Mahmood",
    "Aslam",
    "Akhtar",
    "Nawaz",
    "Rashid",
    "Yousaf",
    "Shah",
    "Mirza",
    "Baig",
    "Hashmi",
    "Bukhari",
    "Haider",
    "Kazmi",
    "Abbas",
    "Awan",
    "Arif",
    "Khalid",
    "Tariq",
    "Nadeem",
    "Saeed",
    "Saleem",
    "Warraich",
    "Gujjar",
    "Cheema",
    "Mughal",
]

CITIES = {
    "Lahore": [
        "Johar Town",
        "DHA Phase 5",
        "Gulberg",
        "Model Town",
        "Wapda Town",
    ],
    "Karachi": [
        "Gulshan-e-Iqbal",
        "Clifton",
        "DHA Phase 6",
        "North Nazimabad",
        "PECHS",
    ],
    "Islamabad": [
        "F-8",
        "F-10",
        "G-11",
        "I-8",
        "E-11",
    ],
    "Rawalpindi": [
        "Satellite Town",
        "Bahria Town",
        "Saddar",
        "Chaklala",
        "PWD",
    ],
    "Faisalabad": [
        "People's Colony",
        "Madina Town",
        "Gulberg",
        "Jinnah Colony",
    ],
    "Multan": [
        "Gulgasht Colony",
        "Cantt",
        "Bosan Road",
        "Shah Rukn-e-Alam",
    ],
    "Peshawar": [
        "Hayatabad",
        "University Town",
        "Saddar",
        "Warsak Road",
    ],
    "Quetta": [
        "Jinnah Town",
        "Satellite Town",
        "Samungli Road",
        "Cantt",
    ],
    "Sialkot": [
        "Cantonment",
        "Model Town",
        "Paris Road",
        "Cantt",
    ],
    "Gujranwala": [
        "Satellite Town",
        "Model Town",
        "DC Colony",
        "Wapda Town",
    ],
    "Bahawalpur": [
        "Model Town",
        "Satellite Town",
        "Dubai Mahal Road",
        "Civil Lines",
        "Commercial Area",
        "Muslim Town",
    ],
    "Sargodha": [
        "Satellite Town",
        "University Road",
        "Model Town",
        "Cantt",
    ],
}

STREETS = [
    "Main Boulevard",
    "College Road",
    "Mall Road",
    "Canal Road",
    "University Road",
    "Jail Road",
    "Circular Road",
    "Jinnah Avenue",
    "Ferozepur Road",
    "GT Road",
]


# ---------------------------------------------------------
# Content
# ---------------------------------------------------------

GENRES = [
    ("Action", "Fast-paced action movies and shows."),
    ("Comedy", "Comedy and light-hearted entertainment."),
    ("Drama", "Character-driven dramatic stories."),
    ("Sci-Fi", "Science fiction and futuristic stories."),
    ("Horror", "Horror and supernatural entertainment."),
    ("Thriller", "Suspenseful and intense stories."),
    ("Romance", "Romantic stories and relationships."),
    ("Adventure", "Adventure and exploration stories."),
    ("Crime", "Crime, investigations and mystery."),
    ("Documentary", "Documentary and factual content."),
]


MOVIES = [
    ("The Last Signal", "A mysterious signal changes the lives of a group of engineers."),
    ("Karachi Nights", "A young journalist uncovers a hidden story during one long night in Karachi."),
    ("Beyond Lahore", "Two friends leave Lahore and discover an unexpected journey."),
    ("The Silent Code", "A software engineer discovers a secret hidden inside an old application."),
    ("Desert Storm", "A team must survive a dangerous expedition through the desert."),
    ("The Forgotten City", "An archaeologist discovers evidence of a lost civilization."),
    ("Final Protocol", "A cybersecurity expert races against time to stop a global attack."),
    ("The Long Road", "A family travels across Pakistan while confronting old conflicts."),
    ("Midnight Train", "Passengers on a midnight train discover something impossible."),
    ("The Last Guardian", "A retired soldier returns to protect his hometown."),
    ("Broken Promise", "Two childhood friends reunite after many years."),
    ("The Deep", "Scientists investigate strange signals coming from the ocean."),
    ("Code Zero", "A programmer becomes involved in a dangerous international operation."),
    ("Hidden Truth", "A detective investigates a case that everyone wants forgotten."),
    ("Mountain Echo", "A documentary filmmaker travels to the northern mountains."),
    ("Second Chance", "A struggling entrepreneur gets an unexpected opportunity."),
    ("Black Horizon", "A group of astronauts face an unknown threat."),
    ("The Missing File", "An ordinary employee discovers a classified document."),
    ("City of Dreams", "Young artists try to build a life in Lahore."),
    ("The Final Game", "A former athlete returns for one final competition."),
    ("Shadow Network", "An investigator uncovers an international criminal network."),
    ("The Visitor", "A mysterious stranger arrives in a quiet town."),
    ("Parallel", "A scientist discovers evidence of another reality."),
    ("After Midnight", "A group of friends experience a night they will never forget."),
    ("The Messenger", "A courier becomes involved in a political conspiracy."),
    ("Lost Expedition", "Explorers disappear while searching for an ancient site."),
    ("Under the Surface", "A journalist investigates corruption inside a powerful company."),
    ("The Crossing", "A family attempts an extraordinary journey."),
    ("Zero Hour", "A security team prepares for a catastrophic event."),
    ("The New Beginning", "A family starts over in a new city."),
]


SHOWS = [
    ("The Startup", "A group of young developers build a technology company."),
    ("City Detectives", "A team of detectives investigates unusual cases."),
    ("The Family", "A comedy-drama about a large Pakistani family."),
    ("Code Room", "Software engineers solve problems while dealing with office life."),
    ("Northern Lights", "A group of travelers explores the northern areas of Pakistan."),
    ("The Agency", "An intelligence team handles dangerous missions."),
    ("Hospital 24", "Doctors and nurses deal with emergencies around the clock."),
    ("The Lawyers", "A group of lawyers takes on complicated cases."),
    ("Campus Life", "Students navigate university, friendships and relationships."),
    ("The Restaurant", "A family tries to save their struggling restaurant."),
    ("Dark Files", "Investigators reopen mysterious unsolved cases."),
    ("The Journalist", "A reporter investigates stories nobody else wants to cover."),
    ("Family Business", "Three siblings fight to save their father's company."),
    ("The Interns", "Young graduates experience their first corporate jobs."),
    ("Borderline", "A team protects a remote region from dangerous threats."),
    ("The Engineers", "A group of engineers work on impossible projects."),
    ("Hidden Room", "A family discovers a mysterious room inside their house."),
    ("The Travelers", "Friends travel across Pakistan looking for adventure."),
    ("The Heist", "A group plans an elaborate robbery."),
    ("Tomorrow", "Scientists work together to prevent a global disaster."),
]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def random_phone():
    return f"+92{random.choice(['300', '301', '302', '303', '304', '305', '306', '307', '308', '309'])}{random.randint(1000000, 9999999)}"


def random_address():
    city = random.choice(list(CITIES.keys()))
    area = random.choice(CITIES[city])
    street = random.choice(STREETS)
    house_number = random.randint(1, 500)

    address = f"House {house_number}, {street}, {area}"

    return city, address


def random_date_of_birth():
    year = random.randint(1975, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return f"{year}-{month:02d}-{day:02d}"


# ---------------------------------------------------------
# Plans
# ---------------------------------------------------------

def create_plans():
    plans = {}

    plan_data = [
        {
            "name": "Free",
            "price": Decimal("0.00"),
            "description": "Browse the catalog but cannot view movie or show descriptions.",
            "can_view_descriptions": False,
            "max_quality": "720p",
        },
        {
            "name": "Standard",
            "price": Decimal("499.00"),
            "description": "View descriptions and stream content in Full HD.",
            "can_view_descriptions": True,
            "max_quality": "1080p",
        },
        {
            "name": "Pro",
            "price": Decimal("999.00"),
            "description": "Premium access with 4K quality and additional features.",
            "can_view_descriptions": True,
            "max_quality": "4K",
        },
    ]

    for data in plan_data:
        plan, _ = Plan.objects.update_or_create(
            name=data["name"],
            defaults=data,
        )

        plans[plan.name] = plan

    print(f"Plans ready: {len(plans)}")

    return plans


# ---------------------------------------------------------
# Genres
# ---------------------------------------------------------

def create_genres():
    genres = {}

    for name, description in GENRES:
        genre, _ = Genre.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
            },
        )

        genres[name] = genre

    print(f"Genres ready: {len(genres)}")

    return genres


# ---------------------------------------------------------
# Movies
# ---------------------------------------------------------

def create_movies(genres):
    movies = []

    for index, (title, description) in enumerate(MOVIES):

        movie, _ = Movie.objects.get_or_create(
            title=title,
            defaults={
                "description": description,
                "release_date": timezone.now().date()
                - timedelta(days=random.randint(30, 3000)),
                "duration": random.randint(80, 180),
                "age_rating": random.choice(
                    ["PG", "PG-13", "16+", "18+"]
                ),
            },
        )

        selected_genres = random.sample(
            list(genres.values()),
            random.randint(1, 3),
        )

        movie.genres.set(selected_genres)

        movies.append(movie)

    print(f"Movies ready: {len(movies)}")

    return movies


# ---------------------------------------------------------
# Shows
# ---------------------------------------------------------

def create_shows(genres):
    shows = []

    for title, description in SHOWS:

        show, _ = Show.objects.get_or_create(
            title=title,
            defaults={
                "description": description,
                "release_date": timezone.now().date()
                - timedelta(days=random.randint(30, 3000)),
                "age_rating": random.choice(
                    ["PG", "PG-13", "16+", "18+"]
                ),
            },
        )

        selected_genres = random.sample(
            list(genres.values()),
            random.randint(1, 3),
        )

        show.genres.set(selected_genres)

        shows.append(show)

    print(f"Shows ready: {len(shows)}")

    return shows


# ---------------------------------------------------------
# Users
# ---------------------------------------------------------

def create_users(plans):
    users_created = 0

    plan_values = list(plans.values())

    for index in range(1, NUM_USERS + 1):

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        username = f"{first_name.lower()}_{last_name.lower()}_{index}"

        email = f"{username}@example.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            },
        )

        if not created:
            continue

        user.set_password(PASSWORD)
        user.save()

        users_created += 1

        city, address = random_address()

        Profile.objects.create(
            user=user,
            phone=random_phone(),
            address=address,
            city=city,
            date_of_birth=random_date_of_birth(),
        )

        # -------------------------------------------------
        # Subscription
        # -------------------------------------------------

        plan = random.choices(
            plan_values,
            weights=[20, 50, 30],
            k=1,
        )[0]

        start_date = timezone.now() - timedelta(
            days=random.randint(1, 180)
        )

        end_date = start_date + timedelta(days=30)

        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status=Subscription.Status.ACTIVE,
        )

        # -------------------------------------------------
        # Payment
        # -------------------------------------------------

        if plan.price > 0:

            Payment.objects.create(
                user=user,
                subscription=subscription,
                amount=plan.price,
                transaction_id=f"TXN-{index:06d}",
                status=Payment.Status.COMPLETED,
            )

        if users_created % 50 == 0:
            print(f"Users created: {users_created}/{NUM_USERS}")

    print(f"Users created: {users_created}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("\nStarting StreamForge database seed...\n")

    plans = create_plans()

    genres = create_genres()

    create_movies(genres)

    create_shows(genres)

    create_users(plans)

    print("\n----------------------------------------")
    print("Database seeding completed!")
    print("----------------------------------------")
    print(f"Users target: {NUM_USERS}")
    print(f"Default password: {PASSWORD}")
    print("----------------------------------------\n")


if __name__ == "__main__":
    main()