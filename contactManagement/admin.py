from django.contrib import admin
from .models import Contacts,Address,Blacklisters
# Register your models here.

admin.site.register(Contacts)
admin.site.register(Address)
admin.site.register(Blacklisters)