from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','is_active','password')
    
    def create(self,data):
        user = User.objects.create(
        username=data['username'],
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name']
        )
        user.set_password(data['password'])
        user.is_active = True
        user.save()
        return user
        
# {
#     "username": "user",
#     "email": "user@user.com",
#     "first_name": "first",
#     "last_name": "dunno",
#     "password": "user"
# }