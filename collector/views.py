from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import CollectorProfile
from client.models import ActivityLog

@login_required(login_url="collector_login")
def collector_dashboard(request):
    collector = request.user
    activities = ActivityLog.objects.filter(user=request.user)[:10]


    try:
        profile = collector.collector_profile
    except CollectorProfile.DoesNotExist:
        profile = None

    context = {
        'collector': collector,
        'profile': profile,
        "activities": activities,
    }

    return render(request, 'collector/dashboard.html', context)

def get_location(request):
    return render(request,'collector/get_location.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import PhotoPost, CollectorAssign
from vendor.models import VendorDetails
from .utils import haversine

@login_required
def nearby_photo_pickups(request):
    collector = request.user

    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not lat or not lng:
        return render(request, "collector/nearby_pickups.html", {
            "error": "Collector location not provided",
            "pickups": []
        })

    lat = float(lat)
    lng = float(lng)
    RADIUS_KM = 5

    # 🔥 Exclude already accepted pickups
    accepted_ids = CollectorAssign.objects.filter(
        collector=collector
    ).values_list("photo_post_id", flat=True)

    results = []

    posts = PhotoPost.objects.exclude(
        id__in=accepted_ids
    ).exclude(
        latitude__isnull=True,
        longitude__isnull=True
    )

    for post in posts:
        distance = haversine(lat, lng, post.latitude, post.longitude)
        if distance <= RADIUS_KM:
            post.distance_km = round(distance, 2)
            results.append(post)

    results.sort(key=lambda x: x.distance_km)

    vendor = VendorDetails.objects.first()

    context = {
        "pickups": results,
        "vendor": vendor,
        "radius": RADIUS_KM,
        "lat": lat,          # 🔥 keep coords
        "lng": lng
    }

    return render(request, "collector/nearby_pickups.html", context)


@login_required
def accept_pickup(request, photo_id):
    collector = request.user

    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    post = get_object_or_404(PhotoPost, id=photo_id)
    vendor = VendorDetails.objects.first()

    distance = haversine(lat, lng, post.latitude, post.longitude)

    CollectorAssign.objects.create(
        collector=collector,
        photo_post=post,
        vendor=vendor,
        pickup_latitude=post.latitude,
        pickup_longitude=post.longitude,
        distance_km=round(distance, 2)
    )

    # 🔥 Redirect back WITH location
    return redirect(f"/collector/nearby-pickups/?lat={lat}&lng={lng}")

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from collector.models import CollectorAssign
from vendor.models import VendorAssignment


# @login_required
# def accept_pickup(request, photo_id):
#     collector = request.user

#     vendor_assignment = get_object_or_404(
#         VendorAssignment,
#         photo_post_id=photo_id
#     )

#     # Prevent duplicate assignment
#     if CollectorAssign.objects.filter(photo_post_id=photo_id).exists():
#         messages.warning(request, "Pickup already assigned.")
#         return redirect("available_pickups")

#     CollectorAssign.objects.create(
#         collector=collector,
#         photo_post=vendor_assignment.photo_post,
#         vendor=vendor_assignment.vendor,
#         pickup_latitude=vendor_assignment.photo_post.latitude,
#         pickup_longitude=vendor_assignment.photo_post.longitude,
#         distance_km=vendor_assignment.distance_km
#     )

#     messages.success(request, "Pickup accepted successfully.")
#     return redirect("accepted_pickups")


@login_required 
def accepted_pickups(request):
    collector = request.user

    assignments = CollectorAssign.objects.filter(
        collector=collector
    ).select_related(
        "photo_post",
        "vendor"
    ).order_by("-accepted_at")

    return render(
        request,
        "collector/accepted_pickups.html",
        {"assignments": assignments}
    )



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from client.models import PhotoPost
from collector.models import CollectorAssign
from client.models import ActivityLog



@login_required
def mark_collected(request, assignment_id):
    assignment = get_object_or_404(
        CollectorAssign,
        id=assignment_id,
        collector=request.user
    )

    photo = assignment.photo_post
    ActivityLog.objects.create(
    user=photo.user,  # client
    activity_type=ActivityLog.ActivityType.PICKUP,
    title="Pickup Collected",
    description=f"{photo.caption or 'E-waste'} picked up"
)

    if photo.status != PhotoPost.Status.COLLECTED:
        photo.status = PhotoPost.Status.COLLECTED
        photo.save()
        messages.success(request, "Pickup marked as collected.")

    return redirect("accepted_pickups")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from collector.models import CollectorAssign
from client.models import PhotoPost


@login_required
def collected_pickups(request):
    collector = request.user

    assignments = (
        CollectorAssign.objects
        .select_related("photo_post", "vendor")
        .filter(
            collector=collector,
            photo_post__status=PhotoPost.Status.COLLECTED
        )
        .order_by("-accepted_at")
    )

    return render(
        request,
        "collector/collected_pickups.html",
        {
            "assignments": assignments,
        }
    )
