from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/<slug:slug>/', views.plan_detail, name='plan_detail'),
    path('checkout/', views.create_checkout_session, name='checkout'),
]