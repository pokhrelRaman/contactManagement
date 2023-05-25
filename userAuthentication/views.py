from django.shortcuts import render,redirect

from rest_framework.response import Response
from rest_framework.views import APIView 

from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer,UpdatePasswordSerializer,UpdateUserSerializer


def loginPage(request):
    return Response("this is login page")

def test(request):
    return redirect('loginPage')


class UserRegistration(APIView):      #user registrations and update user details
    permission_classes = [AllowAny]

    def post(self,request):
        serialized_data = UserSerializer(data = request.data)        
        if serialized_data.is_valid():
            serialized_data.save()
            return Response('User Has been created')
            # redirect 'loginPage.html'
        else :
            errors = serialized_data.errors
            return Response(f'{errors}invalid serializers')
    
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
    permission_classes = (IsAuthenticated)
    authentication_classes = [JWTAuthentication]
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

class ResetPassword(APIView):
    def post(request):
        try:
            username = request.data['username']
            if User.objects.filter(username=username).first():
                
                return Response({'message': 'Resetting email is sent to your account'})
            return Response({'message': "NOT READY YET"})
        except Exception as exception :
            print(exception)
            return Response({'message' : "user not found"})


class Logout(APIView):
    permission_classes = (IsAuthenticated)
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        try:
            token = RefreshToken.for_user(request.user)
            token.blacklist()
            return Response({'message':"user logged out"})
        except Exception as exception:
            return Response("User not found")
        