from django.shortcuts import render
from .models import WorkoutPlan

# Create your views here.
def home(request):
    plans = WorkoutPlan.objects.all()[:3]
    return render(request, 'plans/home.html', {'plans': plans})