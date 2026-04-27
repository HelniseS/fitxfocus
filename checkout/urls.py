from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('create/<slug:slug>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', TemplateView.as_view(template_name='checkout/success.html'), name='checkout_success'),
    path('cancel/', TemplateView.as_view(template_name='checkout/cancel.html'), name='checkout_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]