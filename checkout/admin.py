from django.contrib import admin
from .models import DeliveryOptions,PaymentSelections
# Register your models here.

admin.site.register(PaymentSelections)
admin.site.register(DeliveryOptions)
