from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistration,UserUpdate,ChangePassword,Logout,ResetPassword,loginPage,test



urlpatterns = [
    path('register',UserRegistration.as_view(),name= "registerUser"),
    path('test',test),
    path('contacts/', include('contactManagement.urls')),
    path('update',UserUpdate.as_view()),
    path('changePassword',ChangePassword.as_view()),
    path('logout',Logout.as_view()),
    path('resetPassword',ResetPassword.as_view()),
    path('login', TokenObtainPairView.as_view(), name='loginPage'),
    path('refreshToken', TokenRefreshView.as_view(), name='token_refresh'),


]