from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
import uuid

from .models import Plan, Subscription, Payment


@login_required
def plans_view(request):
    plans = Plan.objects.all().order_by("price")

    return render(
        request,
        "subscriptions/plans.html",
        {"plans": plans},
    )


@login_required
def payment_view(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    if request.method == "POST":
        # Dummy payment
        transaction_id = f"DEMO-{uuid.uuid4().hex[:12].upper()}"

        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=30)

        # Expire existing active subscriptions
        request.user.subscriptions.filter(
            status=Subscription.Status.ACTIVE
        ).update(
            status=Subscription.Status.EXPIRED
        )

        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status=Subscription.Status.ACTIVE,
        )

        Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=plan.price,
            transaction_id=transaction_id,
            status=Payment.Status.COMPLETED,
        )

        messages.success(
            request,
            f"You are now subscribed to the {plan.name} plan.",
        )

        return redirect("profile")

    return render(
        request,
        "subscriptions/payment.html",
        {"plan": plan},
    )
