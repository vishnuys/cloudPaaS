from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Node(models.Model):
    number = models.IntegerField()
    LOAD_LEVEL = [
        ('LOW', 'low'),
        ('MEDIUM', 'medium'),
        ('HIGH', 'high'),
    ]
    load = models.CharField(max_length=10, choices=LOAD_LEVEL, default='LOW')


class Job(models.Model):
    name = models.CharField(max_length=200)
    data_type = models.CharField(max_length=200)
    colname = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    services_order = models.CharField(max_length=200)
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    filepath = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
