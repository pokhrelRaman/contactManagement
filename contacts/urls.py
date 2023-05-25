from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin', admin.site.urls),
    path('user/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/v1.0/refreshToken', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/v1.0/', include('userAuthentication.urls'),name = 'register'),
]
