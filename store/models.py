from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Medicine(models.Model):
    #reference_no = models.AutoField
    Medicine_ID = models.AutoField(primary_key=True)
    Medicine_Name = models.CharField(max_length=50)
    Company_name = models.CharField(max_length=30)
    Company_ID = models.IntegerField(default="null")    
    Manufacturing_date = models.DateField("Mfg Date (MM/DD/YYYY)")
    Expiry_date = models.DateField("Exp Date (MM/DD/YYYY)")
    Price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return str(self.Medicine_ID)
    

# class Sold(models.Model):
#     Purchase_ID = models.AutoField(primary_key=True)
#     Person_ID = models.IntegerField(default=0)
#     Customer_name = models.CharField(max_length=30)
#     Medicine_ID = models.IntegerField(default=0)
#     Medicine_Name = models.CharField(max_length=50)
#     Company_ID = models.IntegerField(default=0) 
#     Company_name = models.CharField(max_length=30)
#     Manufacturing_date = models.DateField("Mfg Date (MM/DD/YYYY)")
#     Expiry_date = models.DateField("Exp Date (MM/DD/YYYY)")
#     Price = models.FloatField()
#     Quantity = models.IntegerField()
#     Bill_amount = models.FloatField()
#     Phone_number = models.IntegerField(default=0)
#     Purchase_date = models.DateField("Purchase Date (MM/DD/YYYY)")

#     def __str__(self):
#         return self.Purchase_ID
    
class Sold(models.Model):
    Company_name = models.CharField(max_length=30)
    Medicine_Name = models.CharField(max_length=50)
    Manufacturing_date = models.DateField("Mfg Date (MM/DD/YYYY)")
    Expiry_date = models.DateField("Exp Date (MM/DD/YYYY)")
    Price = models.FloatField()
    Customer_name = models.CharField(max_length=30)
    Phone_number = models.IntegerField()
    Quantity = models.IntegerField()
    Bill_amount = models.FloatField()
    Purchase_date = models.DateField("Purchase Date (MM/DD/YYYY)")
    Purchase_ID = models.AutoField(primary_key=True)
    Person_ID = models.IntegerField()
    Company_ID = models.IntegerField(default=0)
    Medicine_ID = models.IntegerField(default=0)

    def __str__(self):
        return str(self.Purchase_ID)
    
    