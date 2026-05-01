
import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from plans.models import WorkoutPlan
from .models import Purchase


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_success(request):
    return render(request, "checkout/success.html")


@login_required
def checkout_cancel(request):
    return render(request, "checkout/cancel.html")


@login_required
def create_checkout_session(request, slug):
    plan = get_object_or_404(WorkoutPlan, slug=slug)

    purchase, created = Purchase.objects.get_or_create(
        user=request.user,
        plan=plan,
        defaults={"paid": False},
    )

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": plan.title,
                        "description": plan.short_description,
                    },
                    "unit_amount": int(plan.price * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=request.build_absolute_uri(
            reverse("checkout_success")
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("checkout_cancel")
        ),
        
        client_reference_id=str(request.user.id),
        metadata={
            "plan_id": str(plan.id),
            "plan_slug": plan.slug,
            "user_id": str(request.user.id),
            "purchase_id": str(purchase.id),
        },
    )

    purchase.stripe_checkout_session_id = session.id
    purchase.save()

    return redirect(session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        purchase_id = session.get("metadata", {}).get("purchase_id")

        if purchase_id:
            try:
                purchase = Purchase.objects.get(id=purchase_id)
                purchase.paid = True
                purchase.stripe_checkout_session_id = session.get("id")
                purchase.save()
            except Purchase.DoesNotExist:
                print("Purchase not found")

    return HttpResponse(status=200)
