from django.contrib import admin
from .models import WasteCategory, Waste, Notification

admin.site.register(WasteCategory)
admin.site.register(Waste)
admin.site.register(Notification)