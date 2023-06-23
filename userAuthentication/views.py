from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator,PasswordResetTokenGenerator

from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils.encoding import smart_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt




from .serializers import UserSerializer,UpdatePasswordSerializer,UpdateUserSerializer,ResetPasswordMailSerializer,ResetPasswordSerializer,EmailVerificationSerializer


class UserRegistration(APIView):      #user registrations and update user details
    permission_classes = [AllowAny]

    serializer_class = UserSerializer
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def post(self,request):
        serialized_data = UserSerializer(data = request.data)        
        if serialized_data.is_valid():
            user = serialized_data.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://localhost:8000/auth/v1.0/email/{uid}/{token}"
            print(link)
            return Response({"uid":uid ,"token":token,"link":link})
        return Response(serialized_data.errors, status= status.HTTP_400_BAD_REQUEST)

        
class UserUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UpdateUserSerializer
    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def put(self,request):
        try:
            # user = User.objects.get(id= id)                     mildena user lai afno pk k tha
            user = request.user                                    # jun user le request call garyo tei user instance lai req.user le return garera update garne
            serialized_data = UpdateUserSerializer(instance=user,data=request.data)
            print(serialized_data)
            if serialized_data.is_valid() :
                serialized_data.save()
                return Response('User details has been updated', status= status.HTTP_202_ACCEPTED)
            return Response(f"{serialized_data}")
        except Exception as exception:
            print(exception)
            return Response("User not found", status= status.HTTP_400_BAD_REQUEST)



class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    seriallizer_class = UpdatePasswordSerializer
    @swagger_auto_schema(
        request_body=UpdatePasswordSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self,request):
        user = self.request.user
        serialized_data = UpdatePasswordSerializer(data=request.data)
        if serialized_data.is_valid():
            if not user.check_password(request.data.get('oldPassword')):
                return Response({'message' : "old password is incorrect"})
            user.set_password(request.data.get('newPassword'))
            user.save()
            logout(request)
            return Response({'message': "password sucessfully changed"})
        return Response("invalid Serializer", status=status.HTTP_400_BAD_REQUEST)
        

class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]
    @method_decorator(csrf_exempt)
    def post(self, request):
        try:
            token = RefreshToken.for_user(request.user)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordMailView(APIView):
    permission_classes = [AllowAny]

    serializer_class = ResetPasswordMailSerializer
    @swagger_auto_schema(
        request_body=ResetPasswordMailSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)

    def post(self,request):
        serializer = ResetPasswordMailSerializer(data = request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email = request.data['email'])
            except User.DoesNotExist:
                return Response({'message':"No user with this email is registered"}, status= status.HTTP_401_UNAUTHORIZED)
            uid = user.id
            uid = urlsafe_base64_encode(force_bytes(uid))
            token = PasswordResetTokenGenerator().make_token(user= user)
            link = f"http://localhost:8000/auth/v1.0/reset/{uid}/{token}"
            print(link)
            return Response({'uid':uid,'token':token})
        return Response(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    
    serializer_class = ResetPasswordSerializer
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self,request):
        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():
            uid = request.data.get('uid')
            token = request.data.get('token')
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(id = uid)
            if user and default_token_generator.check_token(user,token):
                user.set_password(request.data['password'])
                return Response({'message':"Resetting password was successful"},status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class EmailVerificationView(APIView):

    serializer_class = EmailVerificationSerializer

    @swagger_auto_schema(
        request_body=EmailVerificationSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self,request):
        serializer = EmailVerificationSerializer(data = request.data)
        if serializer.is_valid():
            uid = request.data.get('uid')
            token = request.data.get('token')
            uid = urlsafe_base64_decode(uid).decode()
            try :
                user = User.objects.get(id = uid)
            except User.DoesNotExist():
                return Response({'message':"user not found"},status= status.HTTP_404_NOT_FOUND)
            if user and default_token_generator.check_token(user,token):
                user.is_active = True
                user.save()
                return Response({'message' : 'verified'})
            else :
                return Response({'message':"Token is not valid or expired"},status= status.HTTP_401_UNAUTHORIZED)

            


class viewall(APIView):
    def get(self,request):
        users = User.objects.all()
        serialized_data = UserSerializer(users, many=True)
        return Response(serialized_data.data)
    

        # email = "raman@user.com"
        # users = User.objects.filter(email = email)
        # serialized_data = UserSerializer(users, many=True)
        # return Response(serialized_data.data)