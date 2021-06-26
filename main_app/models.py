from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Journal(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Entry(models.Model):
    name = models.CharField(max_length=75)
    date = models.DateField(null=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return self.name