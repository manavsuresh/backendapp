from django.db import models

# Create your models here.


class creds(models.Model):
    username = models.CharField(max_length=100,blank=False,unique=True,primary_key=True)
    password = models.CharField(max_length=100,blank=False)
    email = models.EmailField(blank=False)
    level = models.CharField(max_length=100,default='client',blank=False)