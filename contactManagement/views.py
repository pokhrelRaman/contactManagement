from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Contacts, Address
from .serializer import ContactSerializer,BlackListSerializer,PaginationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from django.core.paginator import Paginator

from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



class ContactView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ContactSerializer  
    @swagger_auto_schema(
        request_body=ContactSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self, request):
        user = request.user
        serializer = ContactSerializer(data=request.data ,  context = {'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'messege': 'created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk = None):
        id = pk
        uid = request.user.id
        if id is not None:
            contact = Contacts.objects.get(id = id, uid = uid)
            serialized_data = ContactSerializer(instance =  contact,data= request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': "contacts Updated"},status=status.HTTP_202_ACCEPTED)
            return Response({'message': "invalid Serializer"}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'message': f"{pk} Couldn't Update"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        uid = request.user.id
        try:
            contact = Contacts.objects.get(uid = uid , id=pk)
            contact.delete()
            return Response({'message': "contact has been deleted"})
        except Exception as exception:
            return Response({'message': "contact not found"},status=status.HTTP_404_NOT_FOUND)

class ViewContacts(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class =PaginationSerializer  
    @swagger_auto_schema(
        request_body=PaginationSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self, request, pk=None):
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
        itemsPerPage = request.data.get('itemsPerPage')                   
        pageNo = request.data.get('pageNo')
        
        paginator = Paginator(contacts, itemsPerPage)
        contacts = paginator.get_page(pageNo)
        serialized_data = ContactSerializer(contacts, many=True)
        return Response(serialized_data.data)


    
class Blacklist(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BlackListSerializer

    @swagger_auto_schema(
        request_body=BlackListSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def put(self,request,pk = None):
        uid = request.user.id
        print(pk)
        if pk is not None:
            try:            
                contact = Contacts.objects.get(id=pk)
                serialized_data = BlackListSerializer(instance = contact, data= request.data)
                if serialized_data.is_valid():
                    contact.blacklist = request.data['blacklist']
                    contact.blacklistCount = contact.blacklistCount + 1
                    contact.save()
                    return Response ("message: Contact Blacklisted")
                else:
                    return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
            except Exception as exception:
                return Response({'message':"Contact not found to blacklist"}, status= status.HTTP_404_NOT_FOUND)
        else:
            return Response("message: cannot blacklist unspecified contact",status=status.HTTP_400_BAD_REQUEST)


class ViewBlacklistedUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def get(self,request):
        contacts = Contacts.objects.filter(blacklist= True)
        serialized_data = ContactSerializer(contacts, many = True)
        return Response(serialized_data.data,status= status.HTTP_200_OK)
    



class WhiteListUser(APIView):
    serializer_class = BlackListSerializer
    @swagger_auto_schema(
        request_body=BlackListSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def put(self,request,pk):
        if pk is not None:
            try:
                contact = Contacts.objects.get(id = request.data['id'])
                serialized_data = BlackListSerializer(instance= contact, data = request.data)
                if serialized_data.is_valid():
                    contact.blacklist = request.data['blacklist']
                    contact.blacklistCount = contact.blacklist - 1
                    contact.save()
                    return Response({'message' : " Contact has been removed from blacklist"}, status= status.HTTP_202_ACCEPTED)
                else:
                    return Response(serialized_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
            except Exception as exception:
                return Response({'message':"Contact not found to blacklist"}, status= status.HTTP_404_NOT_FOUND)
        else:
            return Response("message: cannot blacklist unspecified contact",status=status.HTTP_400_BAD_REQUEST)
        


class PublicView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PaginationSerializer
    @swagger_auto_schema(
        request_body=PaginationSerializer,
        responses={200:'NO content'}
        )
    @method_decorator(csrf_exempt)
    
    def post(self,request):
        contacts = Contacts.objects.filter(blacklistCount__lt =  5)
        itemsPerPage = request.data.get('itemsPerPage')                   
        pageNo = request.data.get('pageNo')
        
        paginator = Paginator(contacts, itemsPerPage)
        contacts = paginator.get_page(pageNo)
        pages = paginator.num_pages
        serialized_data = ContactSerializer(contacts, many=True)
        return Response({
        'num_pages': pages,
        'data': list(serialized_data.data)
    })


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


# what if they have mutual contact
# mutual contact wala list banaune ani add garna milyo
# add to mutal contact? use bool ..


#Suggestions:
# pagination, swagger, avatar, whitelisting


#completed 
# Pagination, Avtar, whitelisting, swagger  