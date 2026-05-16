from django import forms
from .models import WorkoutPlan


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = [
            "title",
            "short_description",
            "description",
            "difficulty",
            "duration_weeks",
            "price",
            "is_premium",
            "image",
        ]

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")

        return price

    def clean_duration_weeks(self):
        duration_weeks = self.cleaned_data.get("duration_weeks")

        if duration_weeks is not None and duration_weeks < 1:
            raise forms.ValidationError("Duration must be at least 1 week.")

        return duration_weeks