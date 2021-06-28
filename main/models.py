from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    
