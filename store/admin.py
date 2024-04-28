from django.contrib import admin
from django.contrib.auth.models import User

admin.site.site_header="Pharmacy Management System"

class MedicineAdmin(admin.ModelAdmin):
    list_display = ["Medicine_ID","Medicine_Name","Company_ID","Company_name","Manufacturing_date","Expiry_date","Price", "stock"]
    search_fields = ["Medicine_Name"]

class SoldAdmin(admin.ModelAdmin):
    list_display = ["Purchase_ID","Person_ID","Customer_name","Medicine_ID","Medicine_Name","Company_ID","Company_name","Manufacturing_date","Expiry_date","Price","Quantity", "Bill_amount", "Phone_number", "Purchase_date"]
    search_fields = ["Medicine_Name", "Customer_name"]

# Register your models here.
from .models import Medicine
from .models import Sold



admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Sold, SoldAdmin)

