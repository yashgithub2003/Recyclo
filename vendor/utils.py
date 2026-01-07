from math import radians, sin, cos, asin, sqrt
from accounts.models import VendorDetails
from .models import VendorAssignment
from client.models import PhotoPost


# ============================
# Distance calculation
# ============================
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    R = 6371  # Earth radius in KM
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))

    return R * c


# ============================
# Find nearest vendor
# ============================
def get_nearest_vendor(user_lat, user_lon):
    vendors = VendorDetails.objects.filter(
        is_verified=True,
        latitude__isnull=False,
        longitude__isnull=False,
    )

    if not vendors.exists():
        return None, None

    nearest_vendor = None
    min_distance = float("inf")

    for vendor in vendors:
        distance = haversine_distance(
            user_lat,
            user_lon,
            vendor.latitude,
            vendor.longitude
        )

        if distance < min_distance:
            min_distance = distance
            nearest_vendor = vendor

    return nearest_vendor, min_distance


# ============================
# Assign nearest vendor (PER PHOTO)
# ============================
def assign_nearest_vendor_to_photo(photo_post, user_lat, user_lon):
    vendor, distance_km = get_nearest_vendor(user_lat, user_lon)

    if not vendor:
        return None

    VendorAssignment.objects.create(
        photo_post=photo_post,
        vendor=vendor,
        distance_km=distance_km
    )

    return vendor
