from django.shortcuts import render, get_object_or_404
from .models import WorkoutPlan
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    plans = WorkoutPlan.objects.all()[:3]
    return render(request, 'plans/home.html', {'plans': plans})


def plan_list(request):
    plans = WorkoutPlan.objects.all()
    return render(request, 'plans/plan_list.html', {'plans': plans})


def plan_detail(request, slug):
    plan = get_object_or_404(WorkoutPlan, slug=slug)
    return render(request, 'plans/plan_detail.html', {'plan': plan})


    def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': 'FitXFocus Plan',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/',
        cancel_url='http://127.0.0.1:8000/',
    )
    return redirect(session.url)