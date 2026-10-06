from django.contrib import admin
from .models import Plan, Subscription, Payment

# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "max_quality",
        "can_view_descriptions",
    )

    search_fields = (
        "name",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = (
        "status",
        "plan",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscription",
        "amount",
        "status",
        "transaction_id",
        "created_at",
    )

    search_fields = (
        "user__username",
        "transaction_id",
    )

    list_filter = (
        "status",
    )
