from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import VendorDetails
from client.models import PhotoPost
from vendor.models import VendorAssignment


@login_required(login_url="vendor_login")
def vendor_dashboard(request):
    user = request.user

    # 🔐 Ensure user is vendor
    if not getattr(user, "is_vendor", False):
        messages.error(request, "Unauthorized access.")
        return redirect("vendor_login")

    # ✅ Get vendor profile
    try:
        vendor = VendorDetails.objects.get(user=user)
    except VendorDetails.DoesNotExist:
        messages.error(request, "Vendor profile not found.")
        return redirect("vendor_login")

    # ✅ Get latest assigned photo posts for this vendor
    latest_requests = (
        VendorAssignment.objects
        .select_related("photo_post", "photo_post__user")
        .filter(vendor=vendor)
        .order_by("-assigned_at")[:10]
    )

    # Extract PhotoPost objects (for your template)
    photo_posts = [va.photo_post for va in latest_requests]

    context = {
        "vendor": vendor,
        "latest_requests": photo_posts
    }

    return render(request, "vendor/dashboard.html", context)


@login_required(login_url="vendor_login")
def ewaste_req(request):
    user = request.user

    # 🔒 Ensure vendor role
    if not getattr(user, "is_vendor", False):
        messages.error(request, "Unauthorized access.")
        return redirect("vendor_login")

    # 🔍 Get vendor profile
    try:
        vendor = VendorDetails.objects.get(user=user)
    except VendorDetails.DoesNotExist:
        messages.error(request, "Vendor profile not found.")
        return redirect("vendor_login")

    # ✅ Fetch all assignments for this vendor
    assignments = (
    VendorAssignment.objects
    .select_related("photo_post", "photo_post__user")
    .filter(
        vendor=vendor,
        photo_post__status=PhotoPost.Status.COLLECTED
    )
    .order_by("-assigned_at")
)


    context = {
        "vendor": vendor,
        "assignments": assignments,
    }

    return render(request, "vendor/ewaste_req.html", context)

@login_required(login_url="vendor_login")
def mark_delivered(request, assignment_id):
    assignment = get_object_or_404(
        VendorAssignment,
        id=assignment_id,
        vendor__user=request.user
    )

    photo = assignment.photo_post

    if photo.status == PhotoPost.Status.COLLECTED:
        photo.status = PhotoPost.Status.DELIVERED
        photo.save()
        messages.success(request, "E-waste marked as delivered.")

    else:
        messages.warning(request, "Item must be collected before delivery.")

    return redirect("ewaste_req")

@login_required(login_url="vendor_login")
def delivered_ewaste(request):
    user = request.user

    # 🔒 Ensure vendor role
    if not getattr(user, "is_vendor", False):
        messages.error(request, "Unauthorized access.")
        return redirect("vendor_login")

    # 🔍 Get vendor profile
    try:
        vendor = VendorDetails.objects.get(user=user)
    except VendorDetails.DoesNotExist:
        messages.error(request, "Vendor profile not found.")
        return redirect("vendor_login")

    # ✅ Fetch only:
    # - delivered
    # - assigned to this vendor
    # - report NOT generated yet
    assignments = (
        VendorAssignment.objects
        .select_related("photo_post", "photo_post__user")
        .filter(
            vendor=vendor,
            photo_post__status=PhotoPost.Status.DELIVERED
        )
        .exclude(report__isnull=False)   # <-- 🔥 KEY LINE
        .order_by("-assigned_at")
    )

    context = {
        "vendor": vendor,
        "assignments": assignments,
    }

    return render(request, "vendor/delivered_ewaste.html", context)

# vendor/views.py
from .forms import EwasteReportForm

@login_required(login_url="vendor_login")
def generate_report(request, assignment_id):
    user = request.user

    if not getattr(user, "is_vendor", False):
        messages.error(request, "Unauthorized access.")
        return redirect("vendor_login")

    vendor = get_object_or_404(VendorDetails, user=user)

    assignment = get_object_or_404(
        VendorAssignment,
        id=assignment_id,
        vendor=vendor
    )

    if hasattr(assignment, "report"):
        messages.info(request, "Report already generated.")
        return redirect("delivered_ewaste")

    if request.method == "POST":
        form = EwasteReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.assignment = assignment
            report.save()

            # mark delivered
            photo = assignment.photo_post
            photo.status = PhotoPost.Status.DELIVERED
            photo.save()

            messages.success(request, "Report generated & marked delivered.")
            return redirect("ewaste_req")
    else:
        form = EwasteReportForm()

    return render(request, "vendor/generate_report.html", {
        "form": form,
        "assignment": assignment
    })


@login_required(login_url="vendor_login")
def create_ewaste_report(request, assignment_id):
    assignment = get_object_or_404(VendorAssignment, id=assignment_id)

    # Safety: allow only assigned vendor
    if assignment.vendor.user != request.user:
        return redirect("vendor_dashboard")

    # For now just render page (we will add form next)
    return render(
        request,
        "vendor/create_report.html",
        {
            "assignment": assignment
        }
    )



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EwasteReport, VendorAssignment
from accounts.models import VendorDetails
from client.models import PhotoPost


@login_required(login_url="vendor_login")
def approved_reports(request):
    user = request.user

    if not getattr(user, "is_vendor", False):
        messages.error(request, "Unauthorized access.")
        return redirect("vendor_login")

    vendor = get_object_or_404(VendorDetails, user=user)

    reports = (
        EwasteReport.objects
        .select_related("assignment", "assignment__photo_post", "assignment__photo_post__user")
        .filter(
            assignment__vendor=vendor,
            is_approved_by_client=True
        )
        .order_by("-created_at")
    )

    context = {
        "vendor": vendor,
        "reports": reports,
        "page_title": "Approved Reports"
    }

    return render(request, "vendor/approved_reports.html", context)


@login_required(login_url="vendor_login")
def rejected_reports(request):
    user = request.user

    if not getattr(user, "is_vendor", False):
        messages.error(request, "Unauthorized access.")
        return redirect("vendor_login")

    vendor = get_object_or_404(VendorDetails, user=user)

    reports = (
        EwasteReport.objects
        .select_related("assignment", "assignment__photo_post", "assignment__photo_post__user")
        .filter(
            assignment__vendor=vendor,
            is_approved_by_client=False
        )
        .order_by("-created_at")
    )

    context = {
        "vendor": vendor,
        "reports": reports,
        "page_title": "Rejected Reports"
    }

    return render(request, "vendor/rejected_reports.html", context)
