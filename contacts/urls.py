from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static


from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
   openapi.Info(
      title="Contact Management APIs",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="test License"),
   ),
   public=True,
   permission_classes=[AllowAny],
    authentication_classes=[],
)


urlpatterns = [
    path('admin', admin.site.urls),
    path('auth/v1.0/', include('userAuthentication.urls'),name = 'register'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] +  static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

# schema_view = decorator_with_token_authentication(schema_view)