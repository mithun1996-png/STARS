from django.contrib import admin
from .models import Teacher, MessPG

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'membership_tier',
        'utr_number',
        'payment_status',
        'is_subscription_active',
        'subscription_end_date'
    )
    list_filter = ('membership_tier', 'payment_status', 'verification_level', 'is_featured')
    search_fields = ('name', 'phone', 'utr_number', 'subject')
    actions = ['approve_30_days_subscription', 'reject_invalid_utr']

    @admin.action(description="Approve UPI Payment & Activate Plan (30 Days)")
    def approve_30_days_subscription(self, request, queryset):
        for teacher in queryset:
            teacher.approve_payment(days=30)
        self.message_user(request, f"Successfully approved & activated {queryset.count()} subscription(s).")
    
    @admin.action(description="Reject Selected UTR Payments")
    def reject_invalid_utr(self, request, queryset):
        queryset.update(payment_status='rejected')
        self.message_user(request, f"Marked {queryset.count()} payment(s) as rejected.")
    
@admin.register(MessPG)
class MessPGAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'district', 'rent', 'verified', 'featured')
    list_filter = ('district', 'gender_type', 'verified', 'featured')
    search_fields = ('name', 'owner_name', 'phone', 'location')