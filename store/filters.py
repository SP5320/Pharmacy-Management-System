import django_filters

from .models import *

class MedicineFilter(django_filters.FilterSet):
    Medicine_Name = django_filters.CharFilter(field_name='Medicine_Name', lookup_expr='icontains', label='Medicine Name')
    Company_name = django_filters.CharFilter(field_name='Company_name', lookup_expr='icontains', label='Company Name')
    Company_ID = django_filters.CharFilter(field_name='Company_ID', lookup_expr='icontains', label='Company ID')

    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = ["Manufacturing_date","Expiry_date","Price", "stock"]


class SoldFilter(django_filters.FilterSet):
    Customer_name = django_filters.CharFilter(field_name='Customer_name', lookup_expr='icontains', label='Customer Name')
    Phone_number = django_filters.CharFilter(field_name='Phone_number', lookup_expr='icontains', label='Phone Number' )
    Purchase_date = django_filters.CharFilter(field_name='Purchase_date', lookup_expr='icontains', label='Purchase Date(MM/DD/YYYY)')

    class Meta:
        model = Sold
        fields = '__all__'
        exclude = ["Person_ID","Medicine_ID","Medicine_Name","Company_ID","Company_name","Manufacturing_date","Expiry_date","Price","Quantity", "Bill_amount"]