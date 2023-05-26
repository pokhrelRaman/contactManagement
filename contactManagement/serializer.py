from rest_framework import serializers
from .models import Contacts, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'email', 'contact_number', 'addresses','uid','blacklist']

    def create(self, validated_data,uid = None):
        addresses = validated_data.pop('addresses')
        contact = Contacts.objects.create(**validated_data)
        # contact.uid = uid
        for addr in addresses:
            Address.objects.create(address=addr['address'],contact=contact)
        return contact
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name')
        instance.contact_number = validated_data.get('contact_number')
        instance.email = validated_data.get('email')
        addresses_data = validated_data.pop('addresses')
        for address_data in addresses_data:
            try:
                address = Address.objects.get(contact = instance.id,id = address_data.id)
                address.address = address_data['address']
            except :
                 Address.objects.create(address=address_data['address'],contact=instance)
            address.save()
        return instance
    
class BlackListSerializer(serializers.ModelSerializer):
    def update(self,instance,data):
        instance.blacklist = data['blacklist']
        instance.save()
        return instance