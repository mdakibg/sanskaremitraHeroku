from django.db import models

# Create your models here.
class CustomerRecord(models.Model):
    name = models.CharField(max_length=64)
    mobile = models.CharField(max_length=10)
    service = models.CharField(max_length=25)
    subservice = models.CharField(max_length=25)
    payment = models.IntegerField()
    advance = models.IntegerField(default=0)
    priority = models.CharField(max_length=6)
    status = models.CharField(max_length=10, default='Due')
    date = models.DateField(auto_now_add=True, blank=False)
