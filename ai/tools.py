import sqlite3
from pathlib import Path

from langchain.tools import tool


DB_PATH = "/home/workspace/learning/AI_Support_Eng/data/support.db"


def get_connection():
    """
    Create a connection to the support database.
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@tool
def find_customer(first_name: str, last_name: str) -> dict:
    """
    Find a customer using their first and last name.

    Use this tool when you need to identify a customer before
    retrieving their subscription, invoices, orders, or tickets.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                first_name,
                last_name,
                username,
                email,
                city,
                created_at
            FROM customers
            WHERE LOWER(first_name) = LOWER(?)
              AND LOWER(last_name) = LOWER(?)
            """,
            (first_name.strip(), last_name.strip()),
        )

        customers = cursor.fetchall()

        if not customers:
            return {
                "found": False,
                "message": (
                    f"No customer found with name "
                    f"'{first_name} {last_name}'."
                ),
            }

        if len(customers) > 1:
            return {
                "found": False,
                "multiple_matches": True,
                "message": (
                    f"Multiple customers found with name "
                    f"'{first_name} {last_name}'."
                ),
                "customers": [dict(customer) for customer in customers],
            }

        return {
            "found": True,
            "customer": dict(customers[0]),
        }

    finally:
        connection.close()

@tool
def get_customer_subscription(customer_id: int) -> dict:
    """
    Get the current subscription information for a customer.

    Returns the customer's plan, subscription status, start date,
    renewal date, and plan limits.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                s.id AS subscription_id,
                s.status,
                s.start_date,
                s.renewal_date,

                p.id AS plan_id,
                p.name AS plan_name,
                p.price,
                p.max_team_members,
                p.storage_limit_gb

            FROM subscriptions s

            JOIN plans p
                ON p.id = s.plan_id

            WHERE s.customer_id = ?

            ORDER BY s.start_date DESC

            LIMIT 1
            """,
            (customer_id,),
        )

        subscription = cursor.fetchone()

        if subscription is None:
            return {
                "found": False,
                "message": "No subscription found for this customer.",
            }

        return {
            "found": True,
            "subscription": dict(subscription),
        }

    finally:
        connection.close()


@tool
def get_customer_invoices(
    customer_id: int,
    limit: int = 3,
) -> dict:
    """
    Get a customer's most recent invoices.

    Use this when the customer asks about invoices, billing history,
    invoice status, or recent charges.
    """
    connection = get_connection()

    try:
        # Prevent unreasonable queries.
        limit = min(max(limit, 1), 20)

        cursor = connection.execute(
            """
            SELECT
                id,
                invoice_number,
                amount,
                status,
                issue_date,
                due_date

            FROM invoices

            WHERE customer_id = ?

            ORDER BY issue_date DESC

            LIMIT ?
            """,
            (customer_id, limit),
        )

        invoices = [
            dict(row)
            for row in cursor.fetchall()
        ]

        return {
            "customer_id": customer_id,
            "count": len(invoices),
            "invoices": invoices,
        }

    finally:
        connection.close()


@tool
def get_customer_orders(
    customer_id: int,
    limit: int = 5,
) -> dict:
    """
    Get a customer's recent orders.

    Returns order ID, status, total amount, date, and the products
    contained in each order.
    """
    connection = get_connection()

    try:
        limit = min(max(limit, 1), 20)

        orders_cursor = connection.execute(
            """
            SELECT
                id,
                status,
                total_amount,
                order_date

            FROM orders

            WHERE customer_id = ?

            ORDER BY order_date DESC

            LIMIT ?
            """,
            (customer_id, limit),
        )

        orders = []

        for order in orders_cursor.fetchall():

            items_cursor = connection.execute(
                """
                SELECT
                    p.name AS product_name,
                    oi.quantity,
                    oi.unit_price

                FROM order_items oi

                JOIN products p
                    ON p.id = oi.product_id

                WHERE oi.order_id = ?
                """,
                (order["id"],),
            )

            items = [
                dict(item)
                for item in items_cursor.fetchall()
            ]

            order_data = dict(order)
            order_data["items"] = items

            orders.append(order_data)

        return {
            "customer_id": customer_id,
            "count": len(orders),
            "orders": orders,
        }

    finally:
        connection.close()


@tool
def get_customer_support_tickets(
    customer_id: int,
    status: str | None = None,
) -> dict:
    """
    Get support tickets belonging to a customer.

    Optionally filter tickets by status such as open, in_progress,
    resolved, or closed.
    """
    connection = get_connection()

    try:
        if status:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    category,
                    subject,
                    description,
                    status,
                    priority,
                    created_at

                FROM support_tickets

                WHERE customer_id = ?
                  AND status = ?

                ORDER BY created_at DESC
                """,
                (customer_id, status),
            )

        else:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    category,
                    subject,
                    description,
                    status,
                    priority,
                    created_at

                FROM support_tickets

                WHERE customer_id = ?

                ORDER BY created_at DESC
                """,
                (customer_id,),
            )

        tickets = [
            dict(row)
            for row in cursor.fetchall()
        ]

        return {
            "customer_id": customer_id,
            "count": len(tickets),
            "tickets": tickets,
        }

    finally:
        connection.close()


@tool
def search_products(query: str) -> dict:
    """
    Search available AcmeCloud products and add-ons.

    Use this when the customer asks about available products,
    add-ons, or product prices.
    """
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                price

            FROM products

            WHERE name LIKE ?

            ORDER BY name
            """,
            (f"%{query}%",),
        )

        products = [
            dict(row)
            for row in cursor.fetchall()
        ]

        return {
            "query": query,
            "count": len(products),
            "products": products,
        }

    finally:
        connection.close()


@tool
def get_customer_summary(customer_id: int) -> dict:
    """
    Get a high-level summary of a customer's account.

    Includes basic customer information, subscription information,
    order count, invoice count, and support ticket count.
    """
    connection = get_connection()

    try:
        customer = connection.execute(
            """
            SELECT
                id,
                first_name,
                last_name,
                username,
                email,
                city,
                created_at

            FROM customers

            WHERE id = ?
            """,
            (customer_id,),
        ).fetchone()

        if customer is None:
            return {
                "found": False,
                "message": "Customer not found.",
            }

        subscription = connection.execute(
            """
            SELECT
                p.name AS plan_name,
                s.status,
                s.renewal_date

            FROM subscriptions s

            JOIN plans p
                ON p.id = s.plan_id

            WHERE s.customer_id = ?

            ORDER BY s.start_date DESC

            LIMIT 1
            """,
            (customer_id,),
        ).fetchone()

        order_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM orders
            WHERE customer_id = ?
            """,
            (customer_id,),
        ).fetchone()["count"]

        invoice_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM invoices
            WHERE customer_id = ?
            """,
            (customer_id,),
        ).fetchone()["count"]

        ticket_count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM support_tickets
            WHERE customer_id = ?
            """,
            (customer_id,),
        ).fetchone()["count"]

        return {
            "found": True,
            "customer": dict(customer),
            "subscription": (
                dict(subscription)
                if subscription
                else None
            ),
            "order_count": order_count,
            "invoice_count": invoice_count,
            "ticket_count": ticket_count,
        }

    finally:
        connection.close()

@tool
def search_support_docs(query: str) -> dict:
    """
    Search the AcmeCloud support documentation.

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
    from rag import retriever

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

# Tools exposed to the agent
DATABASE_TOOLS = [
    find_customer,
    get_customer_subscription,
    get_customer_invoices,
    get_customer_orders,
    get_customer_support_tickets,
    search_products,
    get_customer_summary,
    search_support_docs,
]
