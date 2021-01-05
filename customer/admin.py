from django.contrib import admin

from .models import CustomerRecord

# Register your models here.
class ExtendCustomerRecord(admin.ModelAdmin):
    list_display = ('name', 'service', 'subservice', 'payment', 'priority', 'status')


admin.site.register(CustomerRecord, ExtendCustomerRecord)