from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from accounts.models import VendorDetails


from client.models import PhotoPost

class VendorAssignment(models.Model):
    photo_post = models.OneToOneField(
        PhotoPost,
        on_delete=models.CASCADE,
        related_name="vendor_assignment",
        null=True,      # ✅ TEMPORARY
        blank=True      # ✅ TEMPORARY
    )
    vendor = models.ForeignKey(VendorDetails, on_delete=models.CASCADE)
    distance_km = models.FloatField()
    assigned_at = models.DateTimeField(auto_now_add=True)

# vendor/models.py

class EwasteReport(models.Model):
    assignment = models.OneToOneField(
        VendorAssignment,
        on_delete=models.CASCADE,
        related_name="report"
    )

    product_condition = models.CharField(max_length=255)
    working_parts = models.TextField()
    non_working_parts = models.TextField(blank=True)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)

    # ✅ Client approval
    is_approved_by_client = models.BooleanField(null=True,blank=True)
    client_feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.assignment.photo_post.id}"
