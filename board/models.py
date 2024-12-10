from django.db import models
from mdeditor.fields import MDTextField
# Create your models here.
class Type(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class Report(models.Model):
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.title
    
class notice(models.Model):
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=100, blank=True, default="")
    content = MDTextField(default="", editable=True, blank=True)

    def __str__(self):
        return self.author