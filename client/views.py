from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from vendor.models import EwasteReport
from .models import PhotoPost
from accounts.models import Account
from vendor.utils import assign_nearest_vendor_to_photo


# ============================
# PhotoPost Form
# ============================
class PhotoPostForm(forms.ModelForm):
    class Meta:
        model = PhotoPost
        fields = ['photo', 'caption', 'latitude', 'longitude', 'location_name']

    def clean(self):
        cleaned = super().clean()
        lat = cleaned.get("latitude")
        lon = cleaned.get("longitude")

        if lat is None or lon is None:
            raise forms.ValidationError("Location is required to assign a vendor.")

        return cleaned

from client.models import ActivityLog


# ============================
# User Dashboard
# ============================
@login_required(login_url="client_login")
def client_dashboard(request):
    current_user = request.user

    if request.method == "POST":
        form = PhotoPostForm(request.POST, request.FILES)

        if form.is_valid():
            photo_post = form.save(commit=False)
            photo_post.user = current_user
            photo_post.save()

            # ✅ Get coordinates safely
            try:
                user_lat = float(form.cleaned_data.get("latitude"))
                user_lon = float(form.cleaned_data.get("longitude"))
            except (TypeError, ValueError):
                messages.error(request, "Invalid coordinates provided.")
                return redirect("client_dashboard")

            # ✅ Assign nearest vendor PER PHOTO
            assigned_vendor = assign_nearest_vendor_to_photo(
                photo_post=photo_post,
                user_lat=user_lat,
                user_lon=user_lon
            )

            if assigned_vendor:
                messages.success(
                    request,
                    f"Photo posted successfully! Vendor '{assigned_vendor.company_name}' assigned."
                )
            else:
                messages.warning(
                    request,
                    "Photo posted successfully, but no nearby vendor was found."
                )

            return redirect("client_dashboard")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = PhotoPostForm()

    # ✅ FETCH RECENT ACTIVITIES (THIS WAS MISSING)
    activities = (
        ActivityLog.objects
        .filter(user=current_user)
        .order_by("-created_at")[:10]
    )

    return render(
        request,
        "client/dashboard.html",
        {
            "form": form,
            "user": current_user,
            "activities": activities,   # ✅ PASS TO TEMPLATE
        },
    )

from django.contrib.auth.decorators import login_required
from client.models import PhotoPost
from vendor.models import VendorAssignment
from collector.models import CollectorAssign


@login_required
def photo_list(request):
    user = request.user

    # ✅ Fetch user's photos
    photos = PhotoPost.objects.filter(user=user).order_by("-created_at")

    # =========================
    # Vendor Assignments
    # =========================
    vendor_assignments = (
        VendorAssignment.objects
        .select_related("vendor")
        .filter(photo_post__in=photos)
    )

    vendor_map = {
        va.photo_post_id: va for va in vendor_assignments
    }

    # =========================
    # Collector Assignments
    # =========================
    collector_assignments = (
        CollectorAssign.objects
        .select_related("collector")
        .filter(photo_post__in=photos)
    )

    collector_map = {
        ca.photo_post_id: ca for ca in collector_assignments
    }

    # =========================
    # Attach data to photos
    # =========================
    for photo in photos:
        # Vendor
        vendor_assignment = vendor_map.get(photo.id)
        if vendor_assignment:
            photo.vendor_name = vendor_assignment.vendor.company_name
            photo.vendor_distance = vendor_assignment.distance_km
        else:
            photo.vendor_name = "No vendor assigned"
            photo.vendor_distance = None

        # Collector
        collector_assignment = collector_map.get(photo.id)
        if collector_assignment:
            collector = collector_assignment.collector
            photo.collector_name = (
                getattr(collector, "name", None)
                or getattr(collector, "username", None)
                or collector.email
            )
        else:
            photo.collector_name = None

    return render(
        request,
        "client/client_post_list.html",
        {
            "photos": photos,
        },
    )

# # client/views.py

# @login_required(login_url="client_login")
# def client_reports(request):
#     user = request.user

#     if not getattr(user, "is_client", False):
#         messages.error(request, "Unauthorized access.")
#         return redirect("client_login")

#     reports = EwasteReport.objects.select_related(
#         "assignment",
#         "assignment__photo_post",
#         "assignment__vendor"
#     ).filter(
#         assignment__photo_post__user=user
#     ).order_by("-created_at")

#     context = {
#         "reports": reports
#     }

#     return render(request, "client/client_reports.html", context)
# # client/views.py

# @login_required(login_url="client_login")
# def approve_report(request, report_id):
#     user = request.user

#     report = get_object_or_404(
#         EwasteReport,
#         id=report_id,
#         assignment__photo_post__user=user
#     )

#     report.client_approved = True
#     report.save()

#     messages.success(request, "Report approved successfully.")
#     return redirect("client_reports")


# @login_required(login_url="client_login")
# def view_report(request, photo_id):
#     user = request.user

#     photo = get_object_or_404(
#         PhotoPost,
#         id=photo_id,
#         user=user,
#         status=PhotoPost.Status.DELIVERED
#     )

#     assignment = get_object_or_404(
#         VendorAssignment,
#         photo_post=photo
#     )

#     report = EwasteReport.objects.filter(assignment=assignment).first()

#     if not report:
#         messages.warning(request, "⚠️ Report not generated yet by vendor.")
#         return redirect("photo_list")   # or client_dashboard

#     context = {
#         "photo": photo,
#         "assignment": assignment,
#         "report": report
#     }

#     return render(request, "client/view_report.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from vendor.models import EwasteReport, VendorAssignment
from client.models import PhotoPost
from django.contrib import messages


@login_required(login_url="client_login")
def view_report(request, photo_id):
    photo = get_object_or_404(PhotoPost, id=photo_id, user=request.user)

    assignment = get_object_or_404(VendorAssignment, photo_post=photo)

    report = get_object_or_404(EwasteReport, assignment=assignment)

    context = {
        "photo": photo,
        "assignment": assignment,
        "report": report,
    }

    return render(request, "client/view_report.html", context)
@login_required(login_url="client_login")
def approve_report(request, report_id):
    report = get_object_or_404(
        EwasteReport,
        id=report_id,
        assignment__photo_post__user=request.user
    )

    report.is_approved_by_client = True
    report.client_feedback = "Approved by client"
    report.save()

    messages.success(request, "✅ Report approved successfully.")
    return redirect("view_report", photo_id=report.assignment.photo_post.id)

@login_required(login_url="client_login")
def reject_report(request, report_id):
    report = get_object_or_404(
        EwasteReport,
        id=report_id,
        assignment__photo_post__user=request.user
    )

    if request.method == "POST":
        feedback = request.POST.get("feedback")

        report.is_approved_by_client = False
        report.client_feedback = feedback
        report.save()

        messages.error(request, "❌ Report rejected.")
        return redirect("view_report", photo_id=report.assignment.photo_post.id)

    return render(request, "client/reject_report.html", {"report": report})
