from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contacts, Address
from .serializer import ContactSerializer,BlackListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# class contactView(viewsets.ModelViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = Contacts.objects.all()
#     serializer_class = contactSerializer

#     def create(self, request, *args, **kwargs):
#         mutable_data = request.data.copy()
#         addresses = mutable_data.pop('addresses', [])

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         contact = serializer.instance
#         for address in addresses:
#             Address.objects.create(contact=contact, address=address)
#         contact.save()

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContactView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try : 
            uid = request.user.id
        except Exception as exception:
            return Response({'message':"unauthorized user cannot create contact"}) 
        serializer = ContactSerializer(data=request.data,uid=uid)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'messege': 'created'}, status=201)
        return Response(serializer.errors)

    def get(self, request, pk=None):
        id = pk
        uid = request.user.id
        if id is not None:
            try:
                contact = Contacts.objects.get(uid = uid , id = id)
                serialized_data = ContactSerializer(contact)
                return Response(serialized_data.data)
            except Exception as exception:
                print(f"{exception} couldn't get contact with specified id")
                return
        contacts = Contacts.objects.get(uid = uid)
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
        return Response({'message': f"{pk} Couldn't Update"})

    def delete(self, request, pk=None):
        uid = request.user.id
        try:
            contact = Contacts.objects.get(id=pk,uid = uid)
            contact.delete()
            return Response({'message': "contact has been deleted"})
        except Exception as exception:
            return Response({'message': "contact not found" })
    
class blacklist(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self,request,pk = None):
        uid = request.user.id
        if pk is not None:
            try:            
                contact = Contacts.objects.get(id=pk, uid = uid)
                serialized_data = BlackListSerializer(instance= contact,data= request.data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response ("message: Contact Blacklisted")
            except Exception as exception:
                return Response({'message':"Contact not found to blacklist"})
        return Response("mseeage: cannot blacklist unspecified contact")



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

