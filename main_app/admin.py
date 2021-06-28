from django.contrib import admin
# Import models here
from .models import Journal, Entry, Note
# Register your models here.
admin.site.register(Journal)
admin.site.register(Entry)
admin.site.register(Note)