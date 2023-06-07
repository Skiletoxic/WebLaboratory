from django.contrib import admin
from .models import *

# Register your models here.
class JournalAdmin(admin.ModelAdmin):
    list_display= ['number',
        'client_name',
        'client_surname',
        'client_phone',        
        'date_time', 
        'is_done', 
        'description', 
        'norma']
    list_editable=['client_name',
        'client_surname',
        'client_phone',]
    filter_horizontal =['analysis_name', 'analysis_cathegory']
    search_fields=['number',
        'client_name',
        'client_surname',
        'is_done']

class StructureAdmin(admin.ModelAdmin):
    list_display= ['name']
    search_fields=['name']

class PriceAdmin(admin.ModelAdmin):
    list_display= ['name',
        'price',
        'norma']
    search_fields=['name',
        'price',
        'norma']


admin.site.register(Journal, JournalAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Structure, StructureAdmin)
admin.site.register(Room)
admin.site.register(Message)


