from django.contrib.gis import admin
from .models import Member 

admin.site.register(Member, admin.GeoModelAdmin)
