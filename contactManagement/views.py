from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contacts, Address
from .serializer import ContactSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

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
        serializer = ContactSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'messege': 'created'}, status=201)
        return Response(serializer.errors)

    def get(self, request, pk=None):
        id = pk
        if id is not None:
            contact = get_object_or_404(Contacts,id=id)
            serialized_data = ContactSerializer(contact)
            return Response(serialized_data.data)
            
        contacts = Contacts.objects.all()
        serialized_data = ContactSerializer(contacts, many=True)
        return Response(serialized_data.data)

    def put(self, request, pk = None):
        id = pk
        if id is not None:
            contact = Contacts.objects.get(id = id)
            serialized_data = ContactSerializer(instance =  contact,data= request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'message': "contacts Updated"})
        return Response({'message': f"{pk} Couldn't Update"})

    def delete(self, request, pk=None):
        contact = Contacts.objects.get(id=pk)
        contact.delete()
        return Response({'message': "contact has been deleted"})

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

