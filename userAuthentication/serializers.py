from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','is_active','password')
    

    def create(self,data):
        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError('User with given email already exists')
        else:
            user = User.objects.create(
            username=data['username'],
            email=data['email'],                     
            first_name=data['first_name'],
            last_name=data['last_name']
            )
            user.set_password(data['password'])
            user.is_active = False
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
        instance.email = data['email']
        instance.save()

        return instance

class UpdatePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(required = True, write_only=True)
    newPassword = serializers.CharField(required = True, write_only=True ) #validators = [validate_password]                    


class ResetPasswordMailSerializer(serializers.Serializer):
    email = serializers.EmailField()




class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    class Meta:
        fields = ['password']

    # def validate(self,data):
    #     password = data['password']
    #     uid = self.context.get('uid')
    #     token = self.context.get('token')

    #     id = smart_str(urlsafe_base64_decode(uid))
    #     user = User.objects.get(id = id)
    #     if not PasswordResetTokenGenerator().check_token(user=user,token=token):
    #         raise ValueError('Token is not valid or expired')
    #     user.set_password(password)
    #     user.save()
    #     return data

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()
            




# {
#     "username": "user",
#     "email": "user@user.com",
#     "first_name": "first",
#     "last_name": "dunno",
#     "password": "user"
# }