from django.db import models

# Create your models here.
from django.db import models


class WorkoutPlan(models.Model):
    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_weeks = models.PositiveIntegerField(default=4)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_premium = models.BooleanField(default=True)
    image = models.ImageField(upload_to='plans/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title