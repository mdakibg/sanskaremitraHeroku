from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/service', null=True, blank=True)
    isExclusive = models.BooleanField(default=False)
    ExclusiveDescription = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class SubService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    fee = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}({self.fee})'