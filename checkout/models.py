from django.conf import settings
from django.db import models

from plans.models import WorkoutPlan


# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'plan')

    def __str__(self):
        return f"{self.user.username} - {self.plan.title}"
