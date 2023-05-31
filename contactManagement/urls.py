from django.urls import path, include
from rest_framework import routers
from .views import ContactView,UnauthorizedView,Blacklist

urlpatterns = [
    path('',ContactView.as_view()),
    path('viewall',UnauthorizedView.as_view()),
    path('<int:pk>/',ContactView.as_view()),
    path('blacklist/<int:pk>',Blacklist.as_view()),
]