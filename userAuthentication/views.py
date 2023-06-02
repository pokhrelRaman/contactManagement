from collections import namedtuple

from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.contrib.auth.tokens import default_token_generator,PasswordResetTokenGenerator

from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer,UpdatePasswordSerializer,UpdateUserSerializer,ResetPasswordMailSerializer,ResetPasswordSerializer,EmailVerificationSerializer


def loginPage(request):
    return Response("this is login page")

def test(request):
    return redirect('loginPage')


class UserRegistration(APIView):      #user registrations and update user details
    permission_classes = [AllowAny]

    def post(self,request):
        serialized_data = UserSerializer(data = request.data)        
        if serialized_data.is_valid():
            user = serialized_data.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://localhost:8000/auth/v1.0/email/{uid}/{token}"
            print(link)
            return Response({"uid":uid ,"token":token,"link":link})
        return Response(serialized_data.errors)

        
class UserUpdate(APIView):
    permission_classes = (IsAuthenticated)
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        responses={204: "No Content"}
    )
    @method_decorator(csrf_exempt)
    def put(self,request):
        try:
            # user = User.objects.get(id= id)                     mildena user lai afno pk k tha
            user = request.user                                    # jun user le request call garyo tei user instance lai req.user le return garera update garne
            serialized_data = UpdateUserSerializer(instance=user,data=request.data)
            if serialized_data.is_valid() :
                serialized_data.save()
                return Response('User details has been updated')
            return Response(f"{serialized_data}")
        except Exception as exception:
            print(exception)
            return Response("User not found")



class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated)

    def put(self,request):
        user = self.request.user
        serialized_data = UpdatePasswordSerializer(data=request.data)
        if serialized_data.is_valid():
            if not user.check_password(serialized_data.validated_data.get('oldPassword')):
                return Response({'message' : "old password is incorrect"})
            user.set_password(serialized_data.validated_data['newPassword'])
            return Response({'message': "password sucessfully changed"})
        return Response("invalid Serializer")
        

# password reset , token refresh , token verification, logout

class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated)
    
    def post(self,request):
        try:
            token = RefreshToken.for_user(request.user)
            token.blacklist()
            return Response({'message':"user logged out"})
        except Exception as exception:
            return Response("User not found")

class ResetPasswordMailView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ResetPasswordMailSerializer(data = request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email = request.data['email'])
            except User.DoesNotExist:
                return Response({'message':"No user with this email is registered"})
            uid = user.id
            uid = urlsafe_base64_encode(force_bytes(uid))
            token = PasswordResetTokenGenerator().make_token(user= user)
            link = f"http://localhost:8000/auth/v1.0/reset/{uid}/{token}"
            print(link)
            return Response({'message':"Email has been send to reset the password"})
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():
            uid = request.data.get('uid')
            token = request.data.get('token')
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(id = uid)
            print(user)
            if not PasswordResetTokenGenerator().check_token(user=user,token=token):
                user.set_password(request.data['password'])
                return Response({'message':"Resetting password was successful"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class EmailVerificationView(APIView):
    def post(self,request):
        serializer = EmailVerificationSerializer(data = request.data)
        if serializer.is_valid():
            uid = request.data.get('uid')
            token = request.data.get('token')
            uid = urlsafe_base64_decode(uid).decode()
            try :
                user = User.objects.get(id = uid)
            except User.DoesNotExist():
                return Response({'message':"user not found"})
            if user and default_token_generator.check_token(user,token):
                user.is_active = True
                return Response({'message' : 'verified'})
            else :
                return Response({'message':"Token is not valid or expired"})

        
        
        # if serializer.is_valid():
        #     return Response({'message': "email verified"})
        
        #     uid = data.get('uid')
        #     token = data.get('token')
        #     try:
        #         uid = urlsafe_base64_decode(uid).decode()
        #         user = User.objects.get(id = uid)
        #     except User.DoesNotExist():
        #         raise ValueError("User not found")
        
        #     if user and default_token_generator.check(user,token):
        #         user.is_active = True
        #     else :
        #      raise ValueError('Token is not valid or expired') 
            
            


class viewall(APIView):
    def get(self,request):
        users = User.objects.all()
        serialized_data = UserSerializer(users, many=True)
        return Response(serialized_data.data)
        # email = "raman@user.com"
        # users = User.objects.filter(email = email)
        # serialized_data = UserSerializer(users, many=True)
        # return Response(serialized_data.data)