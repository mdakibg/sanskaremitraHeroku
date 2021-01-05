from django.contrib import admin
from .models import Service, SubService

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'isExclusive')

class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('name', "service" , 'fee')

admin.site.register(Service, ServiceAdmin)
admin.site.register(SubService, SubServiceAdmin)
