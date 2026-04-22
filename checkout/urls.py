from django.urls import path
from . import views

urlpatterns = [
    path('create/<slug:slug>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]