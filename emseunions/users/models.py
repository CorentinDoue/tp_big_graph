from django.db import models

from unions.models import Union


class User(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    type = models.TextField(blank=True)
    promo = models.IntegerField()
    contibuted_unions = models.ManyToManyField(Union, related_name="contributors")
    personal_unions = models.ManyToManyField(Union, related_name="members")
