from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin', admin.site.urls),
    path('auth/v1.0/', include('userAuthentication.urls'),name = 'register'),
]
