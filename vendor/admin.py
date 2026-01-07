from django.contrib import admin
from .models import VendorAssignment

admin.site.register(VendorAssignment)

# vendor/admin.py

from django.contrib import admin
from .models import EwasteReport

@admin.register(EwasteReport)
class EwasteReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "assignment",
        "estimated_value",
        "is_approved_by_client",
        "created_at"
    )
    list_filter = ("is_approved_by_client", "created_at")
    search_fields = ("assignment__photo_post__caption",)
