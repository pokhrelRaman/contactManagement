from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contacts, Address
from .serializer import ContactSerializer,BlackListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status

class ContactView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = ContactSerializer(data=request.data ,  context = {'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'messege': 'created'}, status=201)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        id = pk
        uid = request.user.id
        if id is not None:
            try:
                contact = Contacts.objects.get(id = id, uid = uid)  
                serialized_data = ContactSerializer(contact)
                return Response(serialized_data.data)
            except Exception as exception:
                print(f"{exception} couldn't get contact with specified id")                
                return Response({'message':"no contact with given id exists"},status = status.HTTP_404_NOT_FOUND) 
                       
        contacts = Contacts.objects.filter(blacklist = False, uid = uid)
        serialized_data = ContactSerializer(contacts, many=True)
        return Response(serialized_data.data)

    def put(self, request, pk = None):
        id = pk
        uid = request.user.id
        if id is not None:
            contact = Contacts.objects.get(id = id, uid = uid)
            serialized_data = ContactSerializer(instance =  contact,data= request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': "contacts Updated"})
        return Response({'message': f"{pk} Couldn't Update"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        uid = request.user.id
        try:
            contact = Contacts.objects.get(uid = uid , id=pk)
            contact.delete()
            return Response({'message': "contact has been deleted"})
        except Exception as exception:
            return Response({'message': "contact not found" },status=status.HTTP_404_NOT_FOUND)
    
class Blacklist(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self,request,pk = None):
        uid = request.user.id
        print(pk)
        if pk is not None:
            try:            
                contact = Contacts.objects.get(id=pk)
                serialized_data = BlackListSerializer(instance = contact, data= request.data)
                print(serialized_data)
                if serialized_data.is_valid():
                    contact.blacklist = request.data['blacklist']
                    contact.save()
                    return Response ("message: Contact Blacklisted")
                else:
                    return Response(serialized_data.error_messages)
            except Exception as exception:
                return Response({'message':"Contact not found to blacklist"})
        else:
            return Response("message: cannot blacklist unspecified contact")
    
class UnauthorizedView(APIView):
    def get(self,request):
        contacts = Contacts.objects.filter(blacklistCount__lt =  5)
        serialized_data = ContactSerializer(contacts, many=True)
        return Response(serialized_data.data)


# {
#     "name": "upd",
#     "email": "e@2.com",
#     "contact_number": "100010",
#     "addresses": [
#         {
#             "address": "12"
#         },
#         {
#             "address": "St"
#         }
#     ]
# }



