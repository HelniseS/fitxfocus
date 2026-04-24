from django.shortcuts import render, get_object_or_404
from .models import WorkoutPlan
from checkout.models import Purchase


def home(request):
    plans = WorkoutPlan.objects.all()[:3]
    return render(request, 'plans/home.html', {'plans': plans})


def plan_list(request):
    plans = WorkoutPlan.objects.all()
    return render(request, 'plans/plan_list.html', {'plans': plans})


def plan_detail(request, slug):
    plan = get_object_or_404(WorkoutPlan, slug=slug)

    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(
            user=request.user,
            plan=plan,
            paid=True
        ).exists()

    return render(request, 'plans/plan_detail.html', {
        'plan': plan,
        'has_purchased': has_purchased
    })