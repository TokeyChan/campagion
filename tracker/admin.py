from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Workflow)
