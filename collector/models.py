from django.db import models
from client.models import PhotoPost
from accounts.models import VendorDetails
from django.conf import settings


# Create your models here.
class CollectorAssign(models.Model):
    collector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collector_assignments"
    )
    photo_post = models.ForeignKey(
        PhotoPost,
        on_delete=models.CASCADE,
        related_name="collector_assignments"
    )
    vendor = models.ForeignKey(
        VendorDetails,
        on_delete=models.CASCADE
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    distance_km = models.FloatField()

    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.collector.email} → Pickup {self.photo_post.id}"
