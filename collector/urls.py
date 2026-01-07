
from django.urls import path,include
from . import views

urlpatterns = [
    path('collector_dashboard/',views.collector_dashboard,name='collector_dashboard' ),
    path('get_location/',views.get_location,name='get_location'),
    path("nearby-pickups/", views.nearby_photo_pickups, name="nearby_photo_pickups"),
    # 2️⃣ Collector accepts a pickup (CREATES CollectorAssign)
    path(
        "accept-pickup/<int:photo_id>/",
        views.accept_pickup,
        name="accept_pickup"
    ),

    # 3️⃣ Collector sees accepted pickups
    path(
        "accepted-pickups/",
        views.accepted_pickups,
        name="accepted_pickups"
    ),

    # 4️⃣ Collector marks pickup as collected
    path(
        "mark-collected/<int:assignment_id>/",
        views.mark_collected,
        name="mark_collected"
    ),
    path(
    "collected-pickups/",
    views.collected_pickups,
    name="collected_pickups"
    ),

]