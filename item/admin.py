from django.contrib import admin

from .models import Item, Building_Type, Building, Campus, Item_type
# Register your models here.
admin.site.register(Item)
admin.site.register(Building)
admin.site.register(Campus)
admin.site.register(Item_type)
admin.site.register(Building_Type)