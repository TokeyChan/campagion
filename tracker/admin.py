from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Workflow)
admin.site.register(Node)
admin.site.register(Line)
admin.site.register(Completer)
admin.site.register(Template)
