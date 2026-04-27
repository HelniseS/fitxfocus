from django.urls import path
from . import views

urlpatterns = [
    path('create/<slug:slug>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('cancel/', views.checkout_cancel, name='checkout_cancel'),  # ← ADD THIS
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]