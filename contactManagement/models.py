from django.db import models

class Contacts(models.Model):
    name = models.CharField(max_length= 100,help_text="Full Name")
    email = models.EmailField(unique=True)
    contact_number = models.CharField(unique= True,max_length=13,help_text="format: 9779841333333")
    def __str__(self):
        return self.email

class Address(models.Model):
    contact = models.ForeignKey(Contacts,blank=True,null=True, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField(default="kathmandu")

    def __str__(self):
        return self.address
