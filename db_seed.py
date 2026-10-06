import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


DB_PATH = Path("data/support.db")

random.seed(42)


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

FIRST_NAMES = [
    "Muhammad", "Ahmed", "Ali", "Hassan", "Hussain", "Usman",
    "Hamza", "Bilal", "Talha", "Saad", "Ahsan", "Fahad",
    "Zain", "Danish", "Omer", "Asad", "Salman", "Imran",
    "Arslan", "Shahzaib", "Abdullah", "Yousuf", "Shoaib",
    "Kamran", "Waleed", "Taha", "Rayan", "Muneeb", "Areeb",
    "Sana", "Ayesha", "Fatima", "Maryam", "Hira",
    "Iqra", "Mahnoor", "Laiba", "Zainab", "Sadia",
    "Amna", "Maham", "Anum", "Komal", "Saba",
]

LAST_NAMES = [
    "Khan", "Ahmed", "Ali", "Malik", "Sheikh", "Butt",
    "Raza", "Hussain", "Iqbal", "Siddiqui", "Qureshi",
    "Chaudhry", "Javed", "Aslam", "Nawaz", "Farooq",
    "Akhtar", "Mirza", "Hashmi", "Baig",
]

CITIES = [
    "Lahore",
    "Karachi",
    "Islamabad",
    "Rawalpindi",
    "Faisalabad",
    "Multan",
    "Peshawar",
    "Quetta",
    "Sialkot",
    "Gujranwala",
    "Bahawalpur",
    "Hyderabad",
    "Abbottabad",
    "Sargodha",
]

PLAN_DATA = [
    ("Free", 0.00, 1, 5),
    ("Starter", 999.00, 5, 50),
    ("Professional", 2499.00, 20, 500),
    ("Business", 5999.00, 100, 5000),
]

PRODUCT_DATA = [
    ("Extra Storage 100GB", 499.00),
    ("Extra Storage 500GB", 1499.00),
    ("Priority Support", 799.00),
    ("Team Member Add-on", 399.00),
    ("Advanced Analytics", 999.00),
    ("API Access", 699.00),
]

ORDER_STATUSES = [
    "completed",
    "completed",
    "completed",
    "processing",
    "cancelled",
]

INVOICE_STATUSES = [
    "paid",
    "paid",
    "paid",
    "pending",
    "overdue",
]

TICKET_CATEGORIES = [
    "billing",
    "technical",
    "account",
    "feature_request",
    "subscription",
]

TICKET_STATUSES = [
    "open",
    "in_progress",
    "resolved",
    "closed",
]

TICKET_SUBJECTS = {
    "billing": [
        "Charged twice for subscription",
        "Invoice amount is incorrect",
        "Unable to update payment method",
        "Unexpected billing charge",
    ],
    "technical": [
        "Application is not loading",
        "API requests returning errors",
        "Dashboard is very slow",
        "Unable to upload files",
    ],
    "account": [
        "Cannot access my account",
        "Password reset not working",
        "Need to change account email",
        "Two-factor authentication issue",
    ],
    "feature_request": [
        "Request for dark mode",
        "Would like advanced reporting",
        "Need additional export formats",
        "Request for custom notifications",
    ],
    "subscription": [
        "Want to upgrade subscription",
        "Subscription cancellation request",
        "Feature unavailable on current plan",
        "Subscription renewal question",
    ],
}


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def create_tables(connection):
    cursor = connection.cursor()

    cursor.executescript(
        """
        PRAGMA foreign_keys = ON;

        DROP TABLE IF EXISTS support_tickets;
        DROP TABLE IF EXISTS invoices;
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS subscriptions;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS plans;


        CREATE TABLE plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            max_team_members INTEGER NOT NULL,
            storage_limit_gb INTEGER NOT NULL
        );


        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            created_at TEXT NOT NULL
        );


        CREATE TABLE subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            plan_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            start_date TEXT NOT NULL,
            renewal_date TEXT NOT NULL,

            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (plan_id) REFERENCES plans(id)
        );


        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        );


        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date TEXT NOT NULL,

            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );


        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,

            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );


        CREATE TABLE invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            subscription_id INTEGER,
            invoice_number TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,

            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (subscription_id) REFERENCES subscriptions(id)
        );


        CREATE TABLE support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
        """
    )

    connection.commit()


# ---------------------------------------------------------------------------
# Seed plans and products
# ---------------------------------------------------------------------------

def seed_plans(connection):
    connection.executemany(
        """
        INSERT INTO plans
        (name, price, max_team_members, storage_limit_gb)
        VALUES (?, ?, ?, ?)
        """,
        PLAN_DATA,
    )


def seed_products(connection):
    connection.executemany(
        """
        INSERT INTO products
        (name, price)
        VALUES (?, ?)
        """,
        PRODUCT_DATA,
    )


# ---------------------------------------------------------------------------
# Generate customers
# ---------------------------------------------------------------------------

def generate_unique_username(first_name, last_name, index):
    first = first_name.lower()
    last = last_name.lower()

    return f"{first}_{last}_{index}"


def seed_customers(connection, count=100):
    customers = []

    for index in range(1, count + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        username = generate_unique_username(
            first_name,
            last_name,
            index,
        )

        email = f"{username}@example.com"
        city = random.choice(CITIES)

        created_at = (
            datetime.now() - timedelta(days=random.randint(30, 900))
        ).isoformat(timespec="seconds")

        customers.append(
            (
                first_name,
                last_name,
                username,
                email,
                city,
                created_at,
            )
        )

    connection.executemany(
        """
        INSERT INTO customers
        (first_name, last_name, username, email, city, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        customers,
    )

    connection.commit()


# ---------------------------------------------------------------------------
# Generate subscriptions
# ---------------------------------------------------------------------------

def seed_subscriptions(connection):
    cursor = connection.cursor()

    customers = cursor.execute(
        "SELECT id FROM customers"
    ).fetchall()

    plans = cursor.execute(
        "SELECT id FROM plans"
    ).fetchall()

    subscriptions = []

    for (customer_id,) in customers:
        plan_id = random.choice(plans)[0]

        start_date = datetime.now() - timedelta(
            days=random.randint(10, 500)
        )

        renewal_date = start_date + timedelta(days=365)

        status = random.choices(
            ["active", "cancelled", "expired"],
            weights=[80, 10, 10],
        )[0]

        subscriptions.append(
            (
                customer_id,
                plan_id,
                status,
                start_date.date().isoformat(),
                renewal_date.date().isoformat(),
            )
        )

    connection.executemany(
        """
        INSERT INTO subscriptions
        (customer_id, plan_id, status, start_date, renewal_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        subscriptions,
    )

    connection.commit()


# ---------------------------------------------------------------------------
# Generate orders
# ---------------------------------------------------------------------------

def seed_orders(connection):
    cursor = connection.cursor()

    customers = cursor.execute(
        "SELECT id FROM customers"
    ).fetchall()

    products = cursor.execute(
        "SELECT id, price FROM products"
    ).fetchall()

    for (customer_id,) in customers:
        number_of_orders = random.randint(1, 5)

        for _ in range(number_of_orders):
            selected_products = random.sample(
                products,
                random.randint(1, 3),
            )

            order_items = []
            total = 0

            for product_id, price in selected_products:
                quantity = random.randint(1, 2)

                total += price * quantity

                order_items.append(
                    (
                        product_id,
                        quantity,
                        price,
                    )
                )

            order_date = (
                datetime.now()
                - timedelta(days=random.randint(1, 365))
            ).isoformat(timespec="seconds")

            status = random.choice(ORDER_STATUSES)

            cursor.execute(
                """
                INSERT INTO orders
                (customer_id, status, total_amount, order_date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    customer_id,
                    status,
                    round(total, 2),
                    order_date,
                ),
            )

            order_id = cursor.lastrowid

            for product_id, quantity, price in order_items:
                cursor.execute(
                    """
                    INSERT INTO order_items
                    (order_id, product_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        order_id,
                        product_id,
                        quantity,
                        price,
                    ),
                )

    connection.commit()


# ---------------------------------------------------------------------------
# Generate invoices
# ---------------------------------------------------------------------------

def seed_invoices(connection):
    cursor = connection.cursor()

    subscriptions = cursor.execute(
        """
        SELECT
            s.id,
            s.customer_id,
            p.price
        FROM subscriptions s
        JOIN plans p ON p.id = s.plan_id
        """
    ).fetchall()

    for index, (subscription_id, customer_id, amount) in enumerate(
        subscriptions,
        start=1,
    ):
        issue_date = datetime.now() - timedelta(
            days=random.randint(1, 180)
        )

        due_date = issue_date + timedelta(days=30)

        status = random.choice(INVOICE_STATUSES)

        invoice_number = f"INV-{10000 + index}"

        cursor.execute(
            """
            INSERT INTO invoices
            (
                customer_id,
                subscription_id,
                invoice_number,
                amount,
                status,
                issue_date,
                due_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_id,
                subscription_id,
                invoice_number,
                amount,
                status,
                issue_date.date().isoformat(),
                due_date.date().isoformat(),
            ),
        )

    connection.commit()


# ---------------------------------------------------------------------------
# Generate support tickets
# ---------------------------------------------------------------------------

def seed_support_tickets(connection):
    cursor = connection.cursor()

    customers = cursor.execute(
        "SELECT id FROM customers"
    ).fetchall()

    for (customer_id,) in customers:
        number_of_tickets = random.randint(0, 4)

        for _ in range(number_of_tickets):
            category = random.choice(TICKET_CATEGORIES)

            subject = random.choice(
                TICKET_SUBJECTS[category]
            )

            description = (
                f"Customer reported an issue related to: {subject.lower()}. "
                f"Support team needs to investigate the customer's account "
                f"and provide an appropriate resolution."
            )

            status = random.choice(TICKET_STATUSES)

            priority = random.choices(
                ["low", "medium", "high", "urgent"],
                weights=[30, 45, 20, 5],
            )[0]

            created_at = (
                datetime.now()
                - timedelta(days=random.randint(1, 180))
            ).isoformat(timespec="seconds")

            cursor.execute(
                """
                INSERT INTO support_tickets
                (
                    customer_id,
                    category,
                    subject,
                    description,
                    status,
                    priority,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    customer_id,
                    category,
                    subject,
                    description,
                    status,
                    priority,
                    created_at,
                ),
            )

    connection.commit()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)

    try:
        create_tables(connection)

        seed_plans(connection)
        seed_products(connection)
        seed_customers(connection, count=100)
        seed_subscriptions(connection)
        seed_orders(connection)
        seed_invoices(connection)
        seed_support_tickets(connection)

        print(f"Database created successfully: {DB_PATH}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()