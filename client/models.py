from django.db import models
from accounts.models import Account
# Create your models here.
class PhotoPost(models.Model):
    
    class Status(models.TextChoices):
        NOT_PICKED = "not_picked", "Not Picked Up"
        COLLECTED = "collected", "Collected"
        DELIVERED = "delivered", "Delivered"

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='photo_posts')
    photo = models.ImageField(upload_to='e-photos/%Y/%m/%d/')
    caption = models.TextField(blank=True)
    # vendor = models.ForeignKey('vendor.Vendor', on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_PICKED
    )

    location_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    


from django.db import models
from django.conf import settings

class ActivityLog(models.Model):

    class ActivityType(models.TextChoices):
        PICKUP = "pickup", "Pickup Collected"
        PAYMENT = "payment", "Payment Received"
        CERTIFICATE = "certificate", "Certificate Issued"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.title}"
