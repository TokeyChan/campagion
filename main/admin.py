from django.contrib import admin
from main.models import Client, Campaign, User, Department

# Register your models here.
admin.site.register(Client)
admin.site.register(Campaign)
admin.site.register(User)
admin.site.register(Department)
