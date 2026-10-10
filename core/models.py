from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta


class Teacher(models.Model):
    # --- MEMBERSHIP & VERIFICATION TIERS FOR BUSINESS ---
    MEMBERSHIP_TIERS = [
        ('free', 'Basic Profile (Free)'),
        ('pro', 'Teacher Pro (₹299/mo)'),
        ('premium', 'Teacher Premium (₹1,199/mo)'),
    ]

    VERIFICATION_TIERS = [
        ('basic', 'Basic Profile'),
        ('verified', 'Verified Profile'),
        ('professionally_verified', 'Professionally Verified'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('rejected', 'Rejected / Invalid UTR'),
        ('expired', 'Expired'),
    ]

    # --- BASIC PROFILE INFORMATION ---
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    classes = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    fees = models.IntegerField()
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(default=0, help_text="Years of teaching experience")
    photo = models.ImageField(upload_to="teacher_photos/", blank=True, null=True)

    # --- PRO / PREMIUM CONTENT ---
    demo_video = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])],
        blank=True,
        null=True
    )

    # --- METRICS & TRUST STATUS ---
    rating = models.FloatField(default=0.0)
    views = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)  # Quick boolean check
    verification_level = models.CharField(
        max_length=30, 
        choices=VERIFICATION_TIERS, 
        default='basic'
    )

    # --- MONETIZATION, UPI PAYMENT & SUBSCRIPTION SYSTEM ---
    membership_tier = models.CharField(
        max_length=20, 
        choices=MEMBERSHIP_TIERS, 
        default='free'
    )
    is_featured = models.BooleanField(default=False, help_text="Pin profile to the top of listings")
    
    # UPI UTR Verification Fields
    utr_number = models.CharField(
        max_length=12, 
        blank=True, 
        null=True, 
        help_text="12-digit UPI Transaction Reference / UTR Number"
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='active'
    )
    payment_date = models.DateTimeField(blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True, help_text="Date when Pro/Premium expires")

    def is_subscription_active(self):
        """Helper to verify if paid membership is active and verified."""
        if self.membership_tier == 'free':
            return True
        if self.payment_status == 'active' and self.subscription_end_date:
            return self.subscription_end_date > timezone.now()
        return False

    def approve_payment(self, days=30):
        """Helper function for Admin to approve UPI payment in 1 click."""
        self.payment_status = 'active'
        self.payment_date = timezone.now()
        self.subscription_end_date = timezone.now() + timedelta(days=days)
        if self.membership_tier == 'premium':
            self.is_featured = True
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_membership_tier_display()}) - {self.get_payment_status_display()}"


class MessPG(models.Model):
    GENDER_CHOICES = [
        ('Boys', 'Boys'),
        ('Girls', 'Girls'),
        ('Co-ed', 'Co-ed'),
    ]

    ROOM_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple Sharing', 'Triple Sharing'),
        ('Four', 'Four Sharing'),
    ]

    name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    rent = models.IntegerField()
    
    food_available = models.CharField(max_length=50)
    wifi = models.BooleanField(default=False)

    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True)
    description = models.TextField()

    image = models.ImageField(upload_to='mess_images/', null=True, blank=True)
    gender_type = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Boys')
    room_type = models.CharField(max_length=50, choices=ROOM_CHOICES, blank=True, null=True)
    
    google_map_link = models.URLField(
        blank=True,
        help_text="Open Google Maps, click Share, and paste the link here."
    )

    # --- METRICS & TRUST ---
    rating = models.FloatField(default=0.0)
    views = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    featured = models.BooleanField(default=False, help_text="Featured listing on homepage")

    def __str__(self):
        return self.name