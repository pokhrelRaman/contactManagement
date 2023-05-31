from django.db import models
from django.contrib.auth.models import User

class Contacts(models.Model):
    name = models.CharField(max_length= 100,help_text="Full Name")
    email = models.EmailField(unique=True)
    contact_number = models.CharField(unique= True,max_length=13,help_text="format: 9779841333333")
    blacklist = models.BooleanField(default=False)
    blacklistCount = models.IntegerField(default=0)
    uid = models.ForeignKey(User,null=True,on_delete=models.CASCADE )  
    def __str__(self):
        return self.email

class Address(models.Model):
    contact = models.ForeignKey(Contacts,blank=True,null=True, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField(default="kathmandu")

    def __str__(self):
        return self.address
    
# class Blacklist(models.Model):    #kun contact ko ho , koslai blacklist gareko ho 
#     contact = models.ForeignKey(Contacts,blank=True,null=True, on_delete=models.CASCADE, related_name="blacklists")
#     blacklist = models.IntegerField(null=True)

#     def __str__(self): 
#         return self.blacklist
