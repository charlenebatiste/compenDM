from django.contrib import admin
# Import models here
from .models import Journal
# Register your models here.
admin.site.register(Journal)