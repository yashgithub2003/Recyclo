from django.contrib import admin
from .models import PhotoPost

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import PhotoPost

@admin.register(PhotoPost)
class PhotoPostAdmin(admin.ModelAdmin):
    list_filter = (
        'created_at',
    )
    
