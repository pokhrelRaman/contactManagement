from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Contacts, Address,Blacklisters
from .serializer import ContactSerializer,PaginationSerializer, BlacklistersSerializer,WhitelistSerializer
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
        print(uid)
        if id is not None:
            try:
                contact = Contacts.objects.get(id = id, uid = uid)  
                serialized_data = ContactSerializer(contact)
                return Response(serialized_data.data)
            except Exception as exception:
                print(f"{exception} couldn't get contact with specified id")                
                return Response({'message':"no contact with given id exists"},status = status.HTTP_404_NOT_FOUND) 
        blacklist = Blacklisters.objects.filter(uid = uid).values_list('contact')
        print(blacklist)
        contacts = Contacts.objects.exclude(id__in = blacklist).filter(uid = uid)
        itemsPerPage = request.data.get('itemsPerPage')                   
        pageNo = request.data.get('pageNo')
        
        paginator = Paginator(contacts, itemsPerPage)
        contacts = paginator.get_page(pageNo)
        serialized_data = ContactSerializer(contacts, many=True)
        return Response(serialized_data.data)



class ViewBlacklistedUsers_self(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PaginationSerializer

    @swagger_auto_schema(
        request_body=PaginationSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self,request):
        uid = request.user.id
        contacts = []
        blacklisted_contacts = Blacklisters.objects.filter(uid = uid)
        for blacklisted_contact in blacklisted_contacts:
            contact = Contacts.objects.get(id = blacklisted_contact.contact)
            contacts.append(contact)

        itemsPerPage = request.data.get('itemsPerPage')
        pageNo = request.data.get('pageNo')

        paginator = Paginator(contacts, itemsPerPage)
        contacts = paginator.get_page(pageNo)
        pages = paginator.num_pages
        serialized_data = ContactSerializer(contacts, many = True)
        
        return Response({'num_pages': pages,'data':serialized_data.data},status= status.HTTP_200_OK)
    

class TotalBlacklistedUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PaginationSerializer

    @swagger_auto_schema(
        request_body=PaginationSerializer,
        responses={204: "No Content"},
    )
    @method_decorator(csrf_exempt)
    def post(self,request):
        contacts = Contacts.objects.filter(blacklistCount__gt = 0)
        itemsPerPage = request.data.get('itemsPerPage')
        pageNo = request.data.get('pageNo')

        paginator = Paginator(contacts, itemsPerPage)
        contacts = paginator.get_page(pageNo)
        pages = paginator.num_pages
        serialized_data = ContactSerializer(contacts, many = True)
        
        return Response({'num_pages': pages,'data':serialized_data.data},status= status.HTTP_200_OK)
         


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


class Blacklist(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(csrf_exempt)

    def post(self,request,pk):
        uid = request.user.id
        blacklisted_ =  Blacklisters.objects.filter(uid = uid , contact = pk).exists()
        if blacklisted_:
            return Response({'message':"contact was already blaclisted"})
        if Contacts.objects.filter(id = pk).exists:
            serializer = BlacklistersSerializer(data=request.data, context = {'uid': uid, 'contactID': pk})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': "contact has been blacklisted"})
            return Response({'message' : "invalid serializer"}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'message' : "invalid serializer"}, status= status.HTTP_404_NOT_FOUND)
  
class WhitelistUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def post(self,request,pk):
        uid = request.user.id
        blacklist = Blacklisters.objects.filter(uid = uid , contact = pk).exists()
        if blacklist:
            serializer = WhitelistSerializer(data=request.data, context = [{'uid': uid}])
            if serializer.is_valid():
                if blacklist is not None: 
                        blacklist_ = Blacklisters.objects.filter(uid= uid , contact = pk)
                        contact = Contacts.objects.get(id = pk)
                        contact.blacklistCount = contact.blacklistCount - 1
                        contact.save()
                        blacklist_.delete()
                        return Response({'message':"Whitelisted Contact"})
                return Response({'message': "no matching result in blacklist"}, status= status.HTTP_404_NOT_FOUND)
            return Response({'message': " invalid serializer"}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'message': "given contact is not blacklisted by this user"}, status= status.HTTP_404_NOT_FOUND)    
    
###
#Suggestions:
# pagination, swagger, avatar, whitelisting



#completed 
# Pagination, Avtar, whitelisting, swagger
