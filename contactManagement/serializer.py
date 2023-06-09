from rest_framework import serializers
from .models import Contacts, Address


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False)
    class Meta:
        model = Address
        fields = ['id','address','contact']



class ContactSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'email', 'contact_number', 'addresses','uid','blacklist','blacklistCount','avatar']

    def create(self , validated_data):
        user = self.context.get('user')
        addresses = validated_data.pop('addresses')
        contact = Contacts.objects.create(**validated_data)
        contact.uid = user
        contact.save()
        for addr in addresses:
            Address.objects.create(address=addr['address'],contact=contact)
        return contact
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name')
        instance.contact_number = validated_data.get('contact_number')
        instance.email = validated_data.get('email')
        instance.avatar = validated_data.get('avatar')
        addresses_data = validated_data.pop('addresses')
        for address_data in addresses_data:
            try:
                address = Address.objects.get(contact = instance.id,id = address_data.get('id'))
                address.address = address_data['address']
                if address_data['address'] == "":
                    address.delete()
            except :
                 Address.objects.create(address=address_data['address'],contact=instance)      # a method to delete address if no data is send or sth like that 
            address.save()
        instance.save()
        return instance

class BlackListSerializer(serializers.Serializer):
        blacklist = serializers.BooleanField(required=True)
        class Meta:
            fields = ['blacklist']

        def update(self, instance, data):
            blacklist = data['blacklist']
            if blacklist :
                instance.blacklistCount = instance.blacklistCount + 1
                instance.blacklist = True
                print("blacklisted")
            elif instance.blacklistCount < 5 and blacklist is False:
                instance.blacklistCount = instance.blacklistCount - 1
                print("whitelisted")
            instance.blacklist = data['blacklist']
            instance.save()
            return instance