from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.savings_overview, name='savings_overview'),
]
