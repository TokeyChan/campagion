from django.contrib import admin
from main.models import Client, Campaign, User

# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Campaign)
