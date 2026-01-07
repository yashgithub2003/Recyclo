from django.contrib import admin


from django.contrib import admin
from .models import CollectorAssign

@admin.register(CollectorAssign)
class CollectorAssignAdmin(admin.ModelAdmin):
    list_display = (
        "collector",
        "photo_post",
        "vendor",
        "distance_km",
        "accepted_at"
    )
    search_fields = ("collector__email",)
