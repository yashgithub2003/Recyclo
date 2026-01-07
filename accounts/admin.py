from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, ClientProfile,VendorDetails
from django.utils.html import format_html

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active','is_client','is_vendor','is_collector')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'gender',
        'date_of_birth',
        'created_at',
        'updated_at',
    )

    list_select_related = ('user',)

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
    )

    list_filter = (
        'gender',
        'created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': (
                'gender',
                'date_of_birth',
                'address',
                'profile_photo',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


@admin.register(VendorDetails)
class VendorDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'user',
        'contact_person',
        'is_verified',
        'created_at',
    )

    list_filter = (
        'is_verified',
        'created_at',
    )

    search_fields = (
        'company_name',
        'user__email',
        'contact_person',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Vendor Information', {
            'fields': (
                'user',
                'company_name',
                'business_address',
                'contact_person',
                'alternate_phone',
                'profile_photo',
            )
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

from django.contrib import admin
from .models import CollectorProfile


@admin.register(CollectorProfile)
class CollectorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'get_email',
        'get_full_name',
        'date_of_birth',
        'created_at',
    )

    list_select_related = ('user',)

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'user__phone_number',
    )

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Collector Account', {
            'fields': ('user',),
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'address'),
        }),
        ('Documents', {
            'fields': ('profile_photo', 'id_proof'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_full_name(self, obj):
        return obj.user.full_name()
    get_full_name.short_description = 'Full Name'
