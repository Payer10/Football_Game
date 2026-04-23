from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Season)
admin.site.register(Month)
admin.site.register(PlayerWeekdetails)
admin.site.register(PlayerMatch)
admin.site.register(Match)
admin.site.register(News)
