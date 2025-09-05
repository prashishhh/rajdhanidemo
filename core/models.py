

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('reporter', 'Reporter'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    meeting_time = models.DateTimeField()
    meeting_link = models.URLField(blank=True, help_text="Optional online meeting link")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ne', 'Nepali'),
        ('other', 'Other'),
    ]

    headline = models.CharField(max_length=500)
    summary = models.TextField(blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='other')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed (source, url, etc)

    def __str__(self):
        return self.headline[:80]

class EmploymentAd(models.Model):
    """Employment Advertisement model for storing OCR-extracted and manually edited data"""
    
    # Header Information
    title = models.CharField(max_length=200, default="जापानमा रोजगारी")
    person_name = models.CharField(max_length=200, default="Prashish Sapkota", help_text="Name of the person")
    company_name = models.CharField(max_length=200, blank=True)
    pre_approval_date = models.CharField(max_length=50, blank=True)
    chalani_no = models.CharField(max_length=50, blank=True)
    lot_no = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Country Information
    country = models.CharField(max_length=100, default="Kuwait", help_text="Country where the job is located")
    
    # Application Deadline
    application_deadline = models.CharField(max_length=100, blank=True)
    
    # Extra Information (for the bottom table)
    medical_cost_local = models.CharField(max_length=100, default="कामदारले तिर्ने")
    medical_cost_foreign = models.CharField(max_length=100, default="कामदारले तिर्ने")
    insurance_local = models.CharField(max_length=100, default="कामदारले तिर्ने")
    insurance_employment = models.CharField(max_length=100, default="कामदारले तिर्ने")
    air_ticket = models.CharField(max_length=100, default="कामदारले तिर्ने")
    visa_fee = models.CharField(max_length=100, default="कामदारले तिर्ने")
    visa_stamp_fee = models.CharField(max_length=100, default="कामदारले तिर्ने")
    recruitment_fee = models.CharField(max_length=100, default="कामदारले तिर्ने")
    welfare_fund = models.CharField(max_length=100, default="रु. ७०० /-")
    labor_fee = models.CharField(max_length=100, default="कामदारले तिर्ने रु. १५०० /-")
    service_fee = models.CharField(max_length=100, default="कामदारले तिर्ने")
    
    # Extra Notes
    extra_notes = models.TextField(blank=True)
    
    # Interview Information
    interview_custom_text = models.TextField(blank=True, help_text="Custom interview text (leave blank for automatic 8-day calculation)")
    
    # Company Banner Information
    company_logo_text = models.CharField(max_length=50, default="LOGO")
    company_logo_image = models.ImageField(upload_to='company_logos/', blank=True, null=True, help_text="Upload company logo (recommended size: 70x28px)")
    company_banner_image = models.ImageField(upload_to='company_banners/', blank=True, null=True, help_text="Upload company banner (recommended size: 12cm x 1.2cm)")
    company_banner_text = models.CharField(max_length=200, blank=True, help_text="Manual banner text (if no image uploaded)")
    company_banner_title = models.CharField(max_length=200, default="BEST EMPLOYMENT HR SOLUTION")
    company_address = models.CharField(max_length=300, default="ठेगाना: Kathmandu-9, Gaushala, Nepal.")
    company_phone = models.CharField(max_length=100, default="फोन: +977-1-5922788")
    company_email = models.CharField(max_length=200, default="इमेल: info@besthr.com.np, bestemploymenthr123@gmail.com")
    company_website = models.CharField(max_length=100, default="वेब: www.besthr.com.np")
    license_number = models.CharField(max_length=100, default="Gov. Lic. Number 1714/081/082")
    
    # OCR and Processing
    ocr_text = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.country} ({self.created_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        verbose_name = "Employment Advertisement"
        verbose_name_plural = "Employment Advertisements"

class JobPosition(models.Model):
    """Individual job position within an employment advertisement"""
    
    employment_ad = models.ForeignKey(EmploymentAd, on_delete=models.CASCADE, related_name='positions')
    
    # Position Details
    position = models.CharField(max_length=200, blank=True)
    male_count = models.CharField(max_length=10, blank=True)
    female_count = models.CharField(max_length=10, blank=True)
    
    # Salary Information
    salary_amount = models.CharField(max_length=50, blank=True, help_text="Salary amount")
    salary_currency = models.CharField(max_length=10, default="KD", choices=[
        ('KD', 'Kuwaiti Dinar (KD)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('SAR', 'Saudi Riyal (SAR)'),
        ('AED', 'UAE Dirham (AED)'),
        ('QAR', 'Qatar Riyal (QAR)'),
        ('OMR', 'Omani Rial (OMR)'),
        ('BHD', 'Bahraini Dinar (BHD)'),
        ('KWD', 'Kuwaiti Dinar (KWD)'),
        ('NPR', 'Nepali Rupee (रु.)'),
    ])
    salary_npr = models.CharField(max_length=50, blank=True, help_text="Salary in Nepali Rupees (auto-calculated)")
    
    # Work Conditions
    overtime = models.CharField(max_length=100, blank=True)
    hours_per_day = models.CharField(max_length=10, blank=True)
    days_per_week = models.CharField(max_length=10, blank=True)
    yearly_leave = models.CharField(max_length=100, blank=True)
    min_qualification = models.CharField(max_length=200, blank=True)
    food_provided = models.CharField(max_length=10, blank=True)
    housing_provided = models.CharField(max_length=10, blank=True)
    contract_duration = models.CharField(max_length=50, blank=True)
    
    # Order for display
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.position} - {self.employment_ad.company_name}"
    
    class Meta:
        ordering = ['order']
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"

class Interview(models.Model):
    """Interview information for employment advertisements"""
    
    employment_ad = models.ForeignKey(EmploymentAd, on_delete=models.CASCADE, related_name='interviews')
    
    # Interview Details
    interview_type = models.CharField(max_length=50, default="अन्तर्वार्ता", help_text="Type of interview (e.g., अन्तर्वार्ता, मुलाकात)")
    nepali_date = models.CharField(max_length=20, blank=True, help_text="Nepali date (e.g., २०८१/१२/१८)")
    gregorian_date = models.CharField(max_length=20, blank=True, help_text="Gregorian date (e.g., 31 मार्च, 2025)")
    time = models.CharField(max_length=20, blank=True, help_text="Time (e.g., बिहान 11 बजे)")
    location = models.CharField(max_length=200, blank=True, help_text="Location (e.g., म्यानपावरको कार्यालय बसुन्धारामा)")
    
    # Template
    template = models.CharField(max_length=500, default="अन्तरवार्ता मिति {nepali_date} ({gregorian_date}) {location} हुनेछ।")
    
    # Order for display
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Interview {self.order + 1} - {self.employment_ad.company_name}"
    
    def get_formatted_text(self):
        """Return formatted interview text using template"""
        # Handle flexible time display - only show time if it exists
        if self.time:
            template = "अन्तरवार्ता मिति {nepali_date} ({gregorian_date}) {time} {location} हुनेछ।"
        else:
            template = "अन्तरवार्ता मिति {nepali_date} ({gregorian_date}) {location} हुनेछ।"
        
        return template.format(
            nepali_date=self.nepali_date or '',
            gregorian_date=self.gregorian_date or '',
            time=self.time or '',
            location=self.location or ''
        )
    
    class Meta:
        ordering = ['order']
        verbose_name = "Interview"
        verbose_name_plural = "Interviews"

class CurrencyRate(models.Model):
    """Currency exchange rates for automatic conversion"""
    
    currency_code = models.CharField(max_length=10, unique=True, help_text="Currency code (e.g., USD, EUR, GBP)")
    currency_name = models.CharField(max_length=50, help_text="Currency name")
    rate_to_npr = models.DecimalField(max_digits=10, decimal_places=4, help_text="Exchange rate to Nepali Rupees")
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.currency_code} - {self.rate_to_npr} NPR"
    
    class Meta:
        verbose_name = "Currency Rate"
        verbose_name_plural = "Currency Rates"
