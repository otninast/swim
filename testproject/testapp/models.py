from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Tex(models.Model):
    title = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    text = models.TextField(max_length=300, null=True)
    comment = models.TextField(max_length=300, null=True)
    def __str__(self):
        return self.title

class Swimer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generation = models.IntegerField('期')
    
