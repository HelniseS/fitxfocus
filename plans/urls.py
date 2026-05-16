from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('plans/', views.plan_list, name='plan_list'),
    path("create/", views.create_plan, name="create_plan"),
    path('plans/<slug:slug>/', views.plan_detail, name='plan_detail'),
    path("<slug:slug>/edit/", views.edit_plan, name="edit_plan"),
    path("<slug:slug>/delete/", views.delete_plan, name="delete_plan"),  
] 