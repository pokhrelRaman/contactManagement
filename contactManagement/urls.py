from django.urls import path, include
from rest_framework import routers
from .views import ContactView,PublicView,Blacklist,ViewBlacklistedUsers,WhiteListUser,ViewContacts
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',ContactView.as_view()),
    path('viewall',PublicView.as_view()),
    path('<int:pk>',ContactView.as_view()),
    path('<int:pk>',ContactView.as_view()),
    path('myContacts/<int:pk>',ViewContacts.as_view()),
    path('myContacts',ViewContacts.as_view()),
    path('blacklist/<int:pk>',Blacklist.as_view()),
    path('blacklistedUser',ViewBlacklistedUsers.as_view()),
    path('whitelist/<int:pk>',WhiteListUser.as_view()),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)