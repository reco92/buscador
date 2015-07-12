from django.db import models

# Create your models here.


class Info(models.Model):
	titulo = models.CharField(max_length=200)
	tags = models.CharField(max_length=180)
