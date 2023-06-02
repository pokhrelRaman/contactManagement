from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistration,UserUpdate,ChangePassword,Logout,ResetPasswordMailView,loginPage,test,ResetPassword,viewall,EmailVerificationView



urlpatterns = [
    path('register',UserRegistration.as_view(),name= "registerUser"),
    path('update',UserUpdate.as_view()),
    path('changePassword',ChangePassword.as_view()),
    path('logout',Logout.as_view()),
    path('reset',ResetPassword.as_view()),
    path('forgotPassword',ResetPasswordMailView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='loginPage'),
    path('refreshToken', TokenRefreshView.as_view(), name='token_refresh'),
    path('emailVerification',EmailVerificationView.as_view()),
    path('contacts/', include('contactManagement.urls')),
    path('viewalluser', viewall.as_view()),
]