from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Medicine, Sold


class SignupForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AddMedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["Medicine_Name","Company_ID","Company_name","Manufacturing_date","Expiry_date","Price", "stock"]


class SellMedicineForm(forms.ModelForm):
    class Meta:
        model = Sold
        fields = ["Person_ID","Customer_name","Medicine_ID","Medicine_Name","Company_ID","Company_name","Manufacturing_date","Expiry_date","Price","Quantity", "Phone_number", "Purchase_date"]
