from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView 
from .serializers import UserSerializer

def loginPage():
    return Response(f"logged in")


class UserRegistration(APIView):
    
    def post(self,request):
        serialized_data = UserSerializer(data = request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response('User Has been created')
            # redirect 'loginPage.html'
        else :
            errors = serialized_data.errors
            return Response(f'{errors}invalid serializers')

