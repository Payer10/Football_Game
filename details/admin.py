from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(News)
admin.site.register(PlayerRegistration)