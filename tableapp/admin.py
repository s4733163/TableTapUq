from django.contrib import admin
from .models import Vendors, Subscription

@admin.register(Vendors)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email', 'created_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('vendor_username', 'vendor_email', 'start_date', 'end_date', 'is_archived')
    list_filter = ('is_archived', 'start_date')
    search_fields = ('vendor__user__username', 'vendor__user__email')
    ordering = ('-start_date',)

    def vendor_username(self, obj):
        return obj.vendor.user.username
    vendor_username.short_description = 'Username'

    def vendor_email(self, obj):
        return obj.vendor.user.email
    vendor_email.short_description = 'Email'

# Register your models here.
