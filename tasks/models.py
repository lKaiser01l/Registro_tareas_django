
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) #el datetimefield nos permite guardar la fecha y hora, el auto_now_add hace q se agregue automaticamente
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.titulo} - por {self.user.username}'
    

    

