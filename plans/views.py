from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import WorkoutPlan
from checkout.models import Purchase
from .forms import WorkoutPlanForm


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

    return render(request, "plans/plan_detail.html", {
        "plan": plan,
        "has_purchased": has_purchased,
    })

@login_required
def create_plan(request):
    if request.method == "POST":
        form = WorkoutPlanForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("plan_list")
    else:
        form = WorkoutPlanForm()

    return render(request, "plans/create_plan.html", {"form": form})


@login_required
def edit_plan(request, slug):
    plan = get_object_or_404(WorkoutPlan, slug=slug)

    if request.method == "POST":
        form = WorkoutPlanForm(request.POST, request.FILES, instance=plan)

        if form.is_valid():
            form.save()
            return redirect("plan_detail", slug=plan.slug)
    else:
        form = WorkoutPlanForm(instance=plan)

    return render(request, "plans/edit_plan.html", {"form": form, "plan": plan})


@login_required
def delete_plan(request, slug):
    plan = get_object_or_404(WorkoutPlan, slug=slug)

    if request.method == "POST":
        plan.delete()
        return redirect("plan_list")

    return render(request, "plans/delete_plan.html", {"plan": plan})