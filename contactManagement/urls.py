from django.urls import path, include
from rest_framework import routers
from .views import ContactView,UnauthorizedView

urlpatterns = [
    path('',ContactView.as_view()),
    path('viewall',UnauthorizedView.as_view()),
    path('<int:pk>/',ContactView.as_view()),
]