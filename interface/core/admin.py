from django.contrib import admin
from .models import Job, Node, Result

# Register your models here.
admin.site.register(Job)
admin.site.register(Node)
admin.site.register(Result)
