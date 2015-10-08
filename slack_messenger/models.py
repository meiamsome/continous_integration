from django.db import models
from git.models import Repository


# Create your models here.
class SlackBot(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    repositories = models.ManyToManyField(Repository)