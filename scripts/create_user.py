import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal


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
from subscriptions.models import Plan, Subscription, Payment


# =========================================================
# EDIT USER DATA HERE
# =========================================================

USER_DATA = {
    "username": "sadaf_iqbal",
    "email": "sadafiqbal4811@gmail.com",
    "password": "Test12345!",
    "first_name": "Sadaf",
    "last_name": "Iqbal",

    # Profile
    "phone": "+923001234567",
    "address": "House 25, Main Road, Muslim Town",
    "city": "Bahawalpur",
    "date_of_birth": "2001-08-17",

    # Subscription
    "plan": "Pro",
    "subscription_status": "active",

    # Payment
    "payment_status": "completed",
}


# =========================================================
# USER CREATION
# =========================================================

def create_user():
    print("\nCreating user...\n")

    if User.objects.filter(
        username=USER_DATA["username"]
    ).exists():

        print(
            f"User '{USER_DATA['username']}' already exists."
        )

        return

    # -----------------------------------------------------
    # User
    # -----------------------------------------------------

    user = User.objects.create_user(
        username=USER_DATA["username"],
        email=USER_DATA["email"],
        password=USER_DATA["password"],
        first_name=USER_DATA["first_name"],
        last_name=USER_DATA["last_name"],
    )

    print(f"User created: {user.username}")

    # -----------------------------------------------------
    # Profile
    # -----------------------------------------------------

    date_of_birth = datetime.strptime(
        USER_DATA["date_of_birth"],
        "%Y-%m-%d",
    ).date()

    Profile.objects.create(
        user=user,
        phone=USER_DATA["phone"],
        address=USER_DATA["address"],
        city=USER_DATA["city"],
        date_of_birth=date_of_birth,
    )

    print("Profile created.")

    # -----------------------------------------------------
    # Plan
    # -----------------------------------------------------

    try:
        plan = Plan.objects.get(
            name=USER_DATA["plan"]
        )

    except Plan.DoesNotExist:
        print(
            f"Plan '{USER_DATA['plan']}' does not exist."
        )

        user.delete()

        print("User creation rolled back.")

        return

    # -----------------------------------------------------
    # Subscription
    # -----------------------------------------------------

    start_date = datetime.now()

    end_date = start_date + timedelta(days=30)

    subscription = Subscription.objects.create(
        user=user,
        plan=plan,
        start_date=start_date,
        end_date=end_date,
        status=USER_DATA["subscription_status"],
    )

    print(
        f"Subscription created: {plan.name}"
    )

    # -----------------------------------------------------
    # Payment
    # -----------------------------------------------------

    if plan.price > Decimal("0.00"):

        transaction_id = (
            f"MANUAL-{user.id}-{int(start_date.timestamp())}"
        )

        Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=plan.price,
            transaction_id=transaction_id,
            status=USER_DATA["payment_status"],
        )

        print("Payment created.")

    print("\nUser creation completed!")
    print("--------------------------------")
    print(f"Username: {user.username}")
    print(f"Email:    {user.email}")
    print(f"Plan:     {plan.name}")
    print(f"City:     {USER_DATA['city']}")
    print("--------------------------------")


if __name__ == "__main__":
    create_user()