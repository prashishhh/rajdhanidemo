from django.core.management.base import BaseCommand
from core.models import EmploymentAd, JobPosition


class Command(BaseCommand):
    help = 'Clean all default values from EmploymentAd and JobPosition models'

    def handle(self, *args, **options):
        self.stdout.write('🧹 Starting cleanup of default values...')
        
        # Clean EmploymentAd records
        employment_ads = EmploymentAd.objects.all()
        cleaned_ads = 0
        
        for ad in employment_ads:
            cleaned = False
            
            # Clear default values
            if ad.title and ad.title.strip():
                ad.title = ''
                cleaned = True
                
            if ad.person_name and ad.person_name.strip():
                ad.person_name = ''
                cleaned = True
                
            if ad.country and ad.country.strip():
                ad.country = ''
                cleaned = True
                
            if ad.company_name and ad.company_name.strip():
                ad.company_name = ''
                cleaned = True
                
            if ad.medical_cost_local and ad.medical_cost_local.strip():
                ad.medical_cost_local = ''
                cleaned = True
                
            if ad.medical_cost_foreign and ad.medical_cost_foreign.strip():
                ad.medical_cost_foreign = ''
                cleaned = True
                
            if ad.insurance_local and ad.insurance_local.strip():
                ad.insurance_local = ''
                cleaned = True
                
            if ad.insurance_employment and ad.insurance_employment.strip():
                ad.insurance_employment = ''
                cleaned = True
                
            if ad.air_ticket and ad.air_ticket.strip():
                ad.air_ticket = ''
                cleaned = True
                
            if ad.visa_fee and ad.visa_fee.strip():
                ad.visa_fee = ''
                cleaned = True
                
            if ad.visa_stamp_fee and ad.visa_stamp_fee.strip():
                ad.visa_stamp_fee = ''
                cleaned = True
                
            if ad.recruitment_fee and ad.recruitment_fee.strip():
                ad.recruitment_fee = ''
                cleaned = True
                
            if ad.welfare_fund and ad.welfare_fund.strip():
                ad.welfare_fund = ''
                cleaned = True
                
            if ad.labor_fee and ad.labor_fee.strip():
                ad.labor_fee = ''
                cleaned = True
                
            if ad.service_fee and ad.service_fee.strip():
                ad.service_fee = ''
                cleaned = True
                
            if ad.company_logo_text and ad.company_logo_text.strip():
                ad.company_logo_text = ''
                cleaned = True
                
            if ad.company_banner_title and ad.company_banner_title.strip():
                ad.company_banner_title = ''
                cleaned = True
                
            if ad.company_address and ad.company_address.strip():
                ad.company_address = ''
                cleaned = True
                
            if ad.company_phone and ad.company_phone.strip():
                ad.company_phone = ''
                cleaned = True
                
            if ad.company_email and ad.company_email.strip():
                ad.company_email = ''
                cleaned = True
                
            if ad.company_website and ad.company_website.strip():
                ad.company_website = ''
                cleaned = True
                
            if ad.license_number and ad.license_number.strip():
                ad.license_number = ''
                cleaned = True
                
            if cleaned:
                ad.save()
                cleaned_ads += 1
        
        # Clean JobPosition records
        job_positions = JobPosition.objects.all()
        cleaned_positions = 0
        
        for pos in job_positions:
            cleaned = False
            
            if pos.position and pos.position.strip():
                pos.position = ''
                cleaned = True
                
            if pos.male_count and pos.male_count.strip():
                pos.male_count = ''
                cleaned = True
                
            if pos.female_count and pos.female_count.strip():
                pos.female_count = ''
                cleaned = True
                
            if pos.salary_amount and pos.salary_amount.strip():
                pos.salary_amount = ''
                cleaned = True
                
            if pos.salary_currency and pos.salary_currency.strip():
                pos.salary_currency = ''
                cleaned = True
                
            if pos.salary_npr and pos.salary_npr.strip():
                pos.salary_npr = ''
                cleaned = True
                
            if pos.overtime and pos.overtime.strip():
                pos.overtime = ''
                cleaned = True
                
            if pos.hours_per_day and pos.hours_per_day.strip():
                pos.hours_per_day = ''
                cleaned = True
                
            if pos.days_per_week and pos.days_per_week.strip():
                pos.days_per_week = ''
                cleaned = True
                
            if pos.yearly_leave and pos.yearly_leave.strip():
                pos.yearly_leave = ''
                cleaned = True
                
            if pos.min_qualification and pos.min_qualification.strip():
                pos.min_qualification = ''
                cleaned = True
                
            if pos.food_provided and pos.food_provided.strip():
                pos.food_provided = ''
                cleaned = True
                
            if pos.housing_provided and pos.housing_provided.strip():
                pos.housing_provided = ''
                cleaned = True
                
            if pos.contract_duration and pos.contract_duration.strip():
                pos.contract_duration = ''
                cleaned = True
                
            if cleaned:
                pos.save()
                cleaned_positions += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Cleanup completed!\n'
                f'   - EmploymentAd records cleaned: {cleaned_ads}\n'
                f'   - JobPosition records cleaned: {cleaned_positions}\n'
                f'   - All default values removed from database'
            )
        )
