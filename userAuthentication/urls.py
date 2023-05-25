from django.urls import path,include
from .views import UserRegistration,UserUpdate,ChangePassword,Logout,ResetPassword



urlpatterns = [
    path('register',UserRegistration.as_view(),name= "registerUser"),
    path('contacts/', include('contactManagement.urls')),
    path('update',UserUpdate.as_view()),
    path('changePassword',ChangePassword.as_view()),
    path('logout',Logout.as_view()),
    path('resetPassword',ResetPassword.as_view()),
]