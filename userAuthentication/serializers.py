from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','is_active','password')
    
    def create(self,data):
        user = User.objects.create(
        username=data['username'],
        email=data['email'],                     #email verification baki
        first_name=data['first_name'],
        last_name=data['last_name']
        )
        user.set_password(data['password'])
        user.is_active = True
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
    def update(self,instance,data):
        print(data)
        instance.username = data['username']
        instance.first_name = data['first_name']
        instance.last_name = data['last_name']
        instance.email = data['email']    # verify garnu parxa email code mail ma pathayera check garne jasto
        instance.save()

        return instance

class UpdatePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(required = True, write_only=True)
    newPassword = serializers.CharField(required = True, write_only=True,validators = [validate_password] )                      # encrypted data how decrypt








 
        
# {
#     "username": "user",
#     "email": "user@user.com",
#     "first_name": "first",
#     "last_name": "dunno",
#     "password": "user"
# }