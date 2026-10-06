from django.urls import path

from . import views


urlpatterns = [
    path("", views.plans_view, name="plans"),
    path(
        "payment/<int:plan_id>/",
        views.payment_view,
        name="payment",
    ),
]