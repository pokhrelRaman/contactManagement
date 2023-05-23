from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView 
from .views import UserRegistration,loginPage


urlpatterns = [
    path('register',UserRegistration.as_view()),
    path('login',loginPage)
]