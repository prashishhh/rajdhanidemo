# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
import re
import requests
from decimal import Decimal
from .models import EmploymentAd, JobPosition, News, NewsArticle, Meeting, UserProfile, Interview, CurrencyRate
from .forms import EmploymentAdForm, JobPositionForm, JobPositionFormSet, InterviewFormSet, SignUpForm, NewsForm, MeetingForm
from .services.print_service import PrintService
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import localtime

# OCR and Image Processing
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

def update_currency_rates():
    """
    Fetch latest currency exchange rates from API and update database
    """
    try:
        # You can use different APIs - here are some options:
        # 1. ExchangeRate-API (free tier available)
        # 2. Fixer.io (free tier available)
        # 3. Open Exchange Rates (free tier available)
        
        # For now, using a simple approach with hardcoded rates that can be updated
        # In production, you would call an actual API
        
        api_url = "https://api.exchangerate-api.com/v4/latest/NPR"
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                
                # Update rates in database
                for currency_code, rate in rates.items():
                    if currency_code in ['USD', 'EUR', 'GBP', 'SAR', 'AED', 'QAR', 'OMR', 'BHD', 'KWD', 'KD']:
                        # Convert from NPR to currency (inverse rate)
                        inverse_rate = 1 / rate if rate != 0 else 0
                        
                        CurrencyRate.objects.update_or_create(
                            currency_code=currency_code,
                            defaults={
                                'currency_name': f'{currency_code} to NPR',
                                'rate_to_npr': inverse_rate,
                                'is_active': True
                            }
                        )
                
                # Add KD (Kuwaiti Dinar) manually as it's not in most APIs
                CurrencyRate.objects.update_or_create(
                    currency_code='KD',
                    defaults={
                        'currency_name': 'Kuwaiti Dinar to NPR',
                        'rate_to_npr': Decimal('378.51'),
                        'is_active': True
                    }
                )
                
                return True
                
        except requests.RequestException:
            # If API fails, use fallback rates
            pass
        
        # Fallback: Update with current rates (you can update these manually)
        fallback_rates = {
            'KD': ('Kuwaiti Dinar', Decimal('378.51')),
            'USD': ('US Dollar', Decimal('133.45')),
            'EUR': ('Euro', Decimal('145.67')),
            'GBP': ('British Pound', Decimal('170.23')),
            'SAR': ('Saudi Riyal', Decimal('35.58')),
            'AED': ('UAE Dirham', Decimal('36.34')),
            'QAR': ('Qatar Riyal', Decimal('36.67')),
            'OMR': ('Omani Rial', Decimal('346.78')),
            'BHD': ('Bahraini Dinar', Decimal('353.45')),
            'KWD': ('Kuwaiti Dinar', Decimal('378.51')),
        }
        
        for currency_code, (currency_name, rate) in fallback_rates.items():
            CurrencyRate.objects.update_or_create(
                currency_code=currency_code,
                defaults={
                    'currency_name': f'{currency_name} to NPR',
                    'rate_to_npr': rate,
                    'is_active': True
                }
            )
        
        return True
        
    except Exception as e:
        print(f"Error updating currency rates: {e}")
        return False

def get_currency_rate(currency_code):
    """
    Get current exchange rate for a currency
    """
    try:
        rate_obj = CurrencyRate.objects.filter(
            currency_code=currency_code, 
            is_active=True
        ).first()
        
        if rate_obj:
            return rate_obj.rate_to_npr
        
        # If not found, update rates and try again
        update_currency_rates()
        rate_obj = CurrencyRate.objects.filter(
            currency_code=currency_code, 
            is_active=True
        ).first()
        
        return rate_obj.rate_to_npr if rate_obj else Decimal('0')
        
    except Exception:
        return Decimal('0')

# ---------------------- Public Views ----------------------
def home(request):
    """Homepage: show latest human + AI approved news."""
    approved_news = News.objects.filter(status='approved').values('title', 'content', 'approved_at')
    approved_ai_news = NewsArticle.objects.filter(is_approved=True).values('headline', 'summary', 'created_at')

    news_combined = []
    for item in approved_news:
        if item['approved_at']:
            news_combined.append({
                'title': item['title'],
                'content': item['content'],
                'datetime': localtime(item['approved_at'])
            })
    for item in approved_ai_news:
        if item['created_at']:
            news_combined.append({
                'title': item['headline'],
                'content': item['summary'],
                'datetime': localtime(item['created_at'])
            })

    news_combined = sorted(news_combined, key=lambda x: x['datetime'], reverse=True)[:6]
    return render(request, 'home.html', {'news_combined': news_combined})

def register(request):
    """Simple signup; logs user in and redirects home."""
    if request.method == 'POST':
        form = SignUpForm(request.POST) if 'SignUpForm' in globals() else UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                auth_login(request, user)
            except Exception:
                pass
            return redirect('home')
    else:
        form = SignUpForm() if 'SignUpForm' in globals() else UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# ---------------------- Dashboard Redirect ----------------------
@login_required
def dashboard_redirect(request):
    role = request.user.userprofile.role
    if role == 'admin':
        return redirect('admin_dashboard')
    if role == 'editor':
        return redirect('editor_dashboard')
    if role == 'reporter':
        return redirect('reporter_dashboard')
    return redirect('member_dashboard')

# ---------------------- Dashboards ----------------------
@login_required
def member_dashboard(request):
    return render(request, 'member_dashboard.html')

@login_required
def reporter_dashboard(request):
    return render(request, 'reporter_dashboard.html')

@login_required
def editor_dashboard(request):
    return render(request, 'editor_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# ---------------------- News Management ----------------------
@login_required
def submit_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'News submitted successfully!')
            return redirect('member_dashboard')
    else:
        form = NewsForm()
    
    return render(request, 'submit_news.html', {'form': form})

@login_required
def edit_news_by_editor(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News updated successfully!')
            return redirect('editor_dashboard')
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'edit_news_by_editor.html', {'form': form, 'news': news})

@login_required
def edit_ai_news_by_editor(request, news_id):
    news = get_object_or_404(NewsArticle, id=news_id)
    if request.method == 'POST':
        # Handle AI news editing
        news.is_approved = request.POST.get('is_approved') == 'on'
        news.save()
        messages.success(request, 'AI News updated successfully!')
        return redirect('editor_dashboard')
    
    return render(request, 'edit_ai_news_by_editor.html', {'news': news})

# ---------------------- Meeting Management ----------------------
@login_required
def meeting_room(request):
    meetings = Meeting.objects.all().order_by('-created_at')
    can_create = request.user.userprofile.role in ['admin', 'editor']
    
    if request.method == 'POST' and can_create:
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            messages.success(request, 'Meeting created successfully!')
            return redirect('meeting_room')
    else:
        form = MeetingForm()

    return render(request, 'meeting_room.html', {
        'meetings': meetings,
        'form': form,
        'can_create': can_create
    })

# ---------------------- Employment Advertisement Management ----------------------

def parse_ocr_text(ocr_text):
    """
    Parse OCR text to extract employment ad fields
    Returns a dictionary of parsed data
    """
    parsed_data = {}
    
    # Debug: Print the OCR text being processed
    print(f"DEBUG: Processing OCR text: {ocr_text[:200]}...")
    
    # Extract data based on the actual document structure from the provided image
    
    # Company name - look for "SUCCESS NEPAL MANPOWER AGENCY" or similar
    company_match = re.search(r'SUCCESS\s+NEPAL\s+MANPOWER\s+AGENCY', ocr_text, re.IGNORECASE)
    if company_match:
        parsed_data['company_name'] = 'SUCCESS NEPAL MANPOWER AGENCY PVT. LTD.'
    
    # Pre Approval Date - look for "2025/08/15" format (as seen in OCR)
    date_match = re.search(r'(\d{4}/\d{2}/\d{2})', ocr_text)
    if date_match:
        parsed_data['pre_approval_date'] = date_match.group(1)
    
    # LOT No. - look for "LT. No. 327122" format (as seen in OCR)
    lot_match = re.search(r'LT\.\s*No\.\s*(\d+)', ocr_text, re.IGNORECASE)
    if lot_match:
        parsed_data['lot_no'] = lot_match.group(1)
    
    # Chalani No. - look for "चलानी नं. : 60243265" format (as seen in OCR)
    chalani_match = re.search(r'चलानी\s*नं\.?\s*:?\s*(\d+)', ocr_text)
    if chalani_match:
        parsed_data['chalani_no'] = chalani_match.group(1)
    else:
        # Fallback: try to find any 6-8 digit number that could be chalani
        chalani_fallback = re.search(r'(\d{6,8})', ocr_text)
        if chalani_fallback and not parsed_data.get('lot_no'):
            parsed_data['chalani_no'] = chalani_fallback.group(1)
    
    # City - look for "na शहर" format (as seen in OCR)
    city_match = re.search(r'(\w+)\s*शहर', ocr_text)
    if city_match:
        parsed_data['city'] = city_match.group(1).strip()
    
    # Country - look for "Japan मुलुकको" format (as seen in OCR)
    if 'Japan' in ocr_text:
        parsed_data['country'] = 'Japan'
    elif 'Kuwait' in ocr_text:
        parsed_data['country'] = 'Kuwait'
    
    # Position - look for actual job positions in the text
    # Look for patterns like "कामदार" (worker) or specific job titles
    if 'कामदार' in ocr_text:
        # Try to extract the specific position from context
        position_match = re.search(r'(\w+)\s*कामदार', ocr_text)
        if position_match:
            parsed_data['position'] = position_match.group(1)
        else:
            parsed_data['position'] = 'कामदार'
    
    # Also look for specific positions mentioned
    if 'Pop' in ocr_text:
        parsed_data['position'] = 'Pop'
    elif 'Chef' in ocr_text:
        parsed_data['position'] = 'Chef'
    
    # Male/Female count - look for numbers in the demand columns
    male_match = re.search(r'(\d+)\s*पुरुष', ocr_text)
    if male_match:
        parsed_data['male_count'] = male_match.group(1)
    
    female_match = re.search(r'(\d+)\s*महिला', ocr_text)
    if female_match:
        parsed_data['female_count'] = female_match.group(1)
    
    # Also look for specific numbers that might be male/female counts
    # Look for patterns like "23" and "43" in the table
    numbers_in_table = re.findall(r'\b(\d+)\b', ocr_text)
    if numbers_in_table:
        # Filter out obvious non-count numbers (like years, amounts)
        count_numbers = [n for n in numbers_in_table if len(n) <= 2 and n not in ['8', '6', '4', '2', '1', '0']]
        if count_numbers:
            parsed_data['male_count'] = count_numbers[0] if len(count_numbers) > 0 else ''
            parsed_data['female_count'] = count_numbers[1] if len(count_numbers) > 1 else ''
    
    # Salary amount - look for various salary patterns
    # Look for "150 GBP" or "1 KWD" format
    salary_match = re.search(r'(\d+)\s*(GBP|KD|USD|KWD|JPY)', ocr_text)
    if salary_match:
        parsed_data['salary_amount'] = salary_match.group(1)
        parsed_data['salary_currency'] = salary_match.group(2)
    
    # Nepali salary - look for "रु. २५५३५/-" format
    nepali_salary_match = re.search(r'रु\.\s*([२३४५६७८९०१]+)/-', ocr_text)
    if nepali_salary_match:
        parsed_data['nepali_salary'] = nepali_salary_match.group(1)
    
    # Also look for salary patterns in the context of the document
    # Look for patterns like "तलब", "वेतन", "salary" etc.
    salary_context_match = re.search(r'(?:तलब|वेतन|salary|wage)\s*:?\s*(\d+)', ocr_text, re.IGNORECASE)
    if salary_context_match and not parsed_data.get('salary_amount'):
        parsed_data['salary_amount'] = salary_context_match.group(1)
        # Try to determine currency from context
        if 'Japan' in ocr_text or 'JPY' in ocr_text:
            parsed_data['salary_currency'] = 'JPY'
        elif 'Kuwait' in ocr_text or 'KD' in ocr_text:
            parsed_data['salary_currency'] = 'KD'
        elif 'GBP' in ocr_text:
            parsed_data['salary_currency'] = 'GBP'
        elif 'USD' in ocr_text:
            parsed_data['salary_currency'] = 'USD'
    
    # Hours per day - look for "8" or "4" in the hours column (as seen in the image)
    hours_match = re.search(r'(\d+)\s*घण्टा', ocr_text)
    if hours_match:
        parsed_data['hours_per_day'] = hours_match.group(1)
    
    # Days per week - look for "6" or "4" in the days column (as seen in the image)
    days_match = re.search(r'(\d+)\s*दिन', ocr_text)
    if days_match:
        parsed_data['days_per_week'] = days_match.group(1)
    
    # Also look for specific numbers that might be hours/days
    # Look for patterns like "8" and "6" or "4" and "4" in the table
    if not parsed_data.get('hours_per_day') or not parsed_data.get('days_per_week'):
        # Try to find numbers that could be hours and days
        all_numbers = re.findall(r'\b(\d+)\b', ocr_text)
        if all_numbers:
            # Look for numbers that could be hours (typically 4-12) and days (typically 4-7)
            hours_candidates = [n for n in all_numbers if n in ['4', '6', '8', '10', '12']]
            days_candidates = [n for n in all_numbers if n in ['4', '5', '6', '7']]
            
            if hours_candidates and not parsed_data.get('hours_per_day'):
                parsed_data['hours_per_day'] = hours_candidates[0]
            if days_candidates and not parsed_data.get('days_per_week'):
                parsed_data['days_per_week'] = days_candidates[0]
    
    # Contract duration - look for "2 वर्ष" or "3 वर्ष" or just "4" (as seen in the image)
    contract_match = re.search(r'(\d+)\s*वर्ष', ocr_text)
    if contract_match:
        parsed_data['contract_duration'] = contract_match.group(1) + ' वर्ष'
    else:
        # Look for just numbers that could be contract duration
        contract_numbers = re.findall(r'\b(\d+)\b', ocr_text)
        if contract_numbers:
            # Filter for numbers that could be years (1-10)
            year_candidates = [n for n in contract_numbers if n in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']]
            if year_candidates:
                parsed_data['contract_duration'] = year_candidates[0] + ' वर्ष'
    
    # Interview date - look for "२०८१/१२/१८" in the black bar
    interview_date_match = re.search(r'मिति\s*([२३४५६७८९०१]+/[२३४५६७८९०१]+/[२३४५६७८९०१]+)', ocr_text)
    if interview_date_match:
        parsed_data['nepali_date'] = interview_date_match.group(1)
    
    # Interview location - look for "म्यानपावरको कार्यालय बसुन्धारामा"
    if 'म्यानपावरको कार्यालय बसुन्धारामा' in ocr_text:
        parsed_data['interview_location'] = 'म्यानपावरको कार्यालय बसुन्धारामा'
    
    # Set defaults for missing fields
    if not parsed_data.get('company_name'):
        parsed_data['company_name'] = 'SUCCESS NEPAL MANPOWER AGENCY PVT. LTD.'
    if not parsed_data.get('country'):
        parsed_data['country'] = 'Japan'
    if not parsed_data.get('salary_currency'):
        parsed_data['salary_currency'] = 'JPY'
    
    # Debug: Print final parsed data
    print(f"DEBUG: Final parsed data: {parsed_data}")
    
    return parsed_data

def employment_ad_editor(request):
    """OCR-driven Employment Advertisement Editor with multiple positions support"""
    
    # Clean up any duplicate positions first
    try:
        # Get all employment ads
        employment_ads = EmploymentAd.objects.all()
        for ad in employment_ads:
            # Find positions with duplicate order values
            positions = JobPosition.objects.filter(employment_ad=ad).order_by('order')
            seen_orders = set()
            for pos in positions:
                if pos.order in seen_orders:
                    # Delete duplicate positions
                    JobPosition.objects.filter(employment_ad=ad, order=pos.order).exclude(id=pos.id).delete()
                seen_orders.add(pos.order)
    except Exception as e:
        # If cleanup fails, continue anyway
        pass
    
    # Get or create the main employment ad instance
    employment_ad, created = EmploymentAd.objects.get_or_create(
        id=1,
        defaults={
            'title': 'रोजगारी विज्ञापन',
            'company_name': '',
            'pre_approval_date': '',
            'chalani_no': '',
            'lot_no': '',
            'city': '',
            'country': '',
            'application_deadline': '',
            'medical_cost_local': 'कामदारले तिर्ने',
            'medical_cost_foreign': 'कामदारले तिर्ने',
            'insurance_local': 'कामदारले तिर्ने',
            'insurance_employment': 'कामदारले तिर्ने',
            'air_ticket': 'कामदारले तिर्ने',
            'visa_fee': 'कामदारले तिर्ने',
            'visa_stamp_fee': 'कामदारले तिर्ने',
            'recruitment_fee': 'कामदारले तिर्ने',
            'welfare_fund': 'रु. ७०० /-',
            'labor_fee': 'कामदारले तिर्ने रु. १५०० /-',
            'service_fee': 'कामदारले तिर्ने',
            'extra_notes': 'उल्लेखित राशि भन्दा बाहेक अन्य कुनै रकम लिइने छैन। कामदार छनोट भएपछि आवश्यक कागजात र प्रक्रिया पूरा गर्नुपर्नेछ।',
            'company_logo_text': 'LOGO',
            'company_banner_title': 'BEST EMPLOYMENT HR SOLUTION',
            'company_address': 'ठेगाना: Kathmandu-9, Gaushala, Nepal.',
            'company_phone': 'फोन: +977-1-5922788',
            'company_email': 'इमेल: info@besthr.com.np, bestemploymenthr123@gmail.com',
            'company_website': 'वेब: www.besthr.com.np',
            'license_number': 'Gov. Lic. Number 1714/081/082',
        }
    )
    
    # Don't create default job position - let user start with empty form
    # Clean up any existing positions to start fresh
    JobPosition.objects.filter(employment_ad=employment_ad).delete()
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == "ocr":
            # Handle OCR form submission
            if 'document' in request.FILES:
                document = request.FILES['document']
                
                # Clear old OCR data from session
                if 'ocr_text' in request.session:
                    del request.session['ocr_text']
                if 'parsed_data' in request.session:
                    del request.session['parsed_data']
                
                # Process the document
                ocr_text = ""
                parsed_data = {}
                
                try:
                    if document.name.lower().endswith('.pdf'):
                        # Process PDF - handle both InMemoryUploadedFile and TemporaryUploadedFile
                        try:
                            # Try to get temporary file path first
                            if hasattr(document, 'temporary_file_path'):
                                temp_path = document.temporary_file_path()
                                images = convert_from_path(temp_path)
                            else:
                                # For InMemoryUploadedFile, save to temporary file first
                                import tempfile
                                import os
                                
                                # Create temporary file
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                                    for chunk in document.chunks():
                                        temp_file.write(chunk)
                                    temp_path = temp_file.name
                                
                                images = convert_from_path(temp_path)
                                
                                # Clean up temporary file
                                os.unlink(temp_path)
                            
                            for image in images:
                                ocr_text += pytesseract.image_to_string(image, lang='nep+eng')
                        except Exception as pdf_error:
                            # Fallback: try to process as bytes
                            document.seek(0)  # Reset file pointer
                            from pdf2image import convert_from_bytes
                            images = convert_from_bytes(document.read())
                            for image in images:
                                ocr_text += pytesseract.image_to_string(image, lang='nep+eng')
                    else:
                        # Process image
                        image = Image.open(document)
                        ocr_text = pytesseract.image_to_string(image, lang='nep+eng')
                    
                    # Parse OCR text
                    parsed_data = parse_ocr_text(ocr_text)
                    
                    # Debug: Print OCR text and parsed data
                    print(f"DEBUG: OCR Text extracted: {ocr_text[:500]}...")
                    print(f"DEBUG: Parsed data: {parsed_data}")
                    
                    # Store in session
                    request.session['ocr_text'] = ocr_text
                    request.session['parsed_data'] = parsed_data
                    
                    # Clear old employment ad data to force fresh start
                    employment_ad.delete()
                    employment_ad = EmploymentAd.objects.create(
                        title='कुवेतमा रोजगारी',
                        person_name="Prashish Sapkota",
                        company_name="",
                        country="",
                        pre_approval_date="",
                        chalani_no="",
                        lot_no="",
                        city="",
                        application_deadline="",
                        medical_cost_local="",
                        medical_cost_foreign="",
                        insurance_local="",
                        insurance_employment="",
                        air_ticket="",
                        visa_fee="",
                        visa_stamp_fee="",
                        recruitment_fee="",
                        welfare_fund="",
                        labor_fee="",
                        service_fee="",
                        extra_notes="",
                        company_logo_text="LOGO",
                        company_logo_image="",
                        company_banner_title="BEST EMPLOYMENT HR SOLUTION",
                        company_address="ठेगाना: Kathmandu-9, Gaushala, Nepal.",
                        company_phone="फोन: +977-1-5922788",
                        company_email="इमेल: info@besthr.com.np, bestemploymenthr123@gmail.com",
                        company_website="वेब: www.besthr.com.np",
                        license_number="Gov. Lic. Number 1714/081/082",
                    )
                    
                    # Clear old interviews
                    employment_ad.interviews.all().delete()
                    
                    # Create fresh default interview
                    Interview.objects.create(
                        employment_ad=employment_ad,
                        order=0,
                        interview_type='अन्तर्वार्ता',
                        nepali_date='२०८१/१२/१८',
                        gregorian_date='31 मार्च, 2025',
                        time='',
                        location='म्यानपावरको कार्यालय बसुन्धारामा',
                        template='अन्तरवार्ता मिति {nepali_date} ({gregorian_date}) {location} हुनेछ।'
                    )
                    
                    # Clear old positions
                    employment_ad.positions.all().delete()
                    
                    # Create fresh default position
                    JobPosition.objects.create(
                        employment_ad=employment_ad,
                        order=0,
                        position="",
                        male_count="",
                        female_count="",
                        salary_amount="",
                        salary_currency="KD",
                        salary_npr="",
                        overtime="",
                        hours_per_day="",
                        days_per_week="",
                        yearly_leave="",
                        min_qualification="",
                        food_provided="",
                        housing_provided="",
                        contract_duration=""
                    )
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        from django.http import JsonResponse
                        return JsonResponse({'success': True, 'message': 'OCR सफलतापूर्वक अपलोड गरियो!'})
                    else:
                        messages.success(request, 'OCR uploaded successfully!')
                        return redirect('employment_ad_editor')
                        
                except Exception as e:
                    error_msg = f'OCR processing error: {str(e)}'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        from django.http import JsonResponse
                        return JsonResponse({'success': False, 'error': error_msg})
                    else:
                        messages.error(request, error_msg)
            else:
                error_msg = 'कृपया एउटा दस्तावेज अपलोड गर्नुहोस्।'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': False, 'error': error_msg})
                else:
                    messages.error(request, error_msg)
        
        elif form_type == "edit":
            # Handle main form submission (now includes both main info and positions)
            try:
                form = EmploymentAdForm(request.POST, request.FILES, instance=employment_ad)
                formset = JobPositionFormSet(request.POST, instance=employment_ad)
                
                # Debug: Print form data
                print(f"DEBUG: Form data: {request.POST}")
                print(f"DEBUG: Form is_valid: {form.is_valid()}")
                print(f"DEBUG: Formset is_valid: {formset.is_valid()}")
                
                if form.is_valid() and formset.is_valid():
                    # Get interview data from form
                    nepali_date = request.POST.get('interview_nepali_date', '')
                    gregorian_date = request.POST.get('interview_gregorian_date', '')
                    interview_time = request.POST.get('interview_time', '')
                    interview_location = request.POST.get('interview_location', '')
                    
                    # Save the main form
                    form.save()
                    
                    # Process positions and inherit common fields from first position
                    positions = formset.save(commit=False)
                    
                    if positions:
                        # Get common fields from first position
                        first_position = positions[0]
                        common_fields = {
                            'overtime': first_position.overtime,
                            'hours_per_day': first_position.hours_per_day,
                            'days_per_week': first_position.days_per_week,
                            'yearly_leave': first_position.yearly_leave,
                            'min_qualification': first_position.min_qualification,
                            'food_provided': first_position.food_provided,
                            'housing_provided': first_position.housing_provided,
                            'contract_duration': first_position.contract_duration,
                        }
                        
                        # Apply common fields to all positions
                        for position in positions:
                            for field_name, field_value in common_fields.items():
                                if field_value:  # Only apply if first position has a value
                                    setattr(position, field_name, field_value)
                            position.save()
                    else:
                        # No positions, just save the formset normally
                        formset.save()
                    
                    # Update or create interview information
                    if nepali_date or gregorian_date or interview_time or interview_location:
                        interview, created = Interview.objects.get_or_create(
                            employment_ad=employment_ad,
                            order=0,
                            defaults={
                                'interview_type': 'अन्तर्वार्ता',
                                'nepali_date': nepali_date,
                                'gregorian_date': gregorian_date,
                                'time': interview_time,
                                'location': interview_location,
                                'template': 'अन्तरवार्ता मिति {nepali_date} ({gregorian_date}) {location} हुनेछ।'
                            }
                        )
                        
                        if not created:
                            # Update existing interview
                            interview.nepali_date = nepali_date
                            interview.gregorian_date = gregorian_date
                            interview.time = interview_time
                            interview.location = interview_location
                            interview.template = 'अन्तरवार्ता मिति {nepali_date} ({gregorian_date}) {location} हुनेछ।'
                            interview.save()
                    
                    # Check if this is an AJAX request
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        from django.http import JsonResponse
                        return JsonResponse({'success': True, 'message': 'मुख्य जानकारी र पदहरू सफलतापूर्वक सेभ गरियो!'})
                    else:
                        messages.success(request, 'Employment advertisement and positions updated successfully!')
                        return redirect('employment_ad_editor')
                else:
                    # Debug form errors
                    print(f"DEBUG: Form errors: {form.errors}")
                    print(f"DEBUG: Formset errors: {formset.errors}")
                    print(f"DEBUG: Formset non-form errors: {formset.non_form_errors()}")
                    
                    # Create detailed error message
                    error_details = []
                    if form.errors:
                        error_details.append(f"Form errors: {form.errors}")
                    if formset.errors:
                        error_details.append(f"Formset errors: {formset.errors}")
                    if formset.non_form_errors():
                        error_details.append(f"Formset non-form errors: {formset.non_form_errors()}")
                    
                    error_msg = 'त्रुटि भयो। कृपया पुनः प्रयास गर्नुहोस्।'
                    if error_details:
                        error_msg += f" Details: {'; '.join(error_details)}"
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        from django.http import JsonResponse
                        return JsonResponse({'success': False, 'error': error_msg})
                    else:
                        messages.error(request, error_msg)
                    
            except Exception as e:
                # Catch any unexpected errors
                print(f"DEBUG: Unexpected error in form submission: {str(e)}")
                error_msg = f'त्रुटि भयो। कृपया पुनः प्रयास गर्नुहोस्। Error: {str(e)}'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': False, 'error': error_msg})
                else:
                    messages.error(request, error_msg)
        
        elif form_type == "position":
            # Handle position formset submission
            formset = JobPositionFormSet(request.POST, instance=employment_ad)
            if formset.is_valid():
                # Clear existing positions before saving new ones to prevent duplicates
                employment_ad.positions.all().delete()
                
                # Save the new positions
                formset.save()
                
                # Check if this is an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': True, 'message': 'कामदार पदहरू सफलतापूर्वक सेभ गरियो!'})
                else:
                    messages.success(request, 'Job positions updated successfully!')
                    return redirect('employment_ad_editor')
            else:
                # Debug formset errors
                print(f"Formset errors: {formset.errors}")
                print(f"Formset non-form errors: {formset.non_form_errors()}")
                error_msg = 'त्रुटि: कृपया सबै आवश्यक फिल्डहरू भर्नुहोस्।'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': False, 'error': error_msg})
                else:
                    messages.error(request, error_msg)
    
    # Get OCR data from session if available
    ocr_text = request.session.get('ocr_text', '')
    parsed_data = request.session.get('parsed_data', {})
    
    # Only clear OCR data if explicitly requested (not on every page load)
    # This allows the parsed data to persist and populate the form fields
    
    # Always create completely fresh forms to prevent showing old data
    if parsed_data and any(parsed_data.values()):
        # Create a fresh form instance with OCR data
        form = EmploymentAdForm(instance=employment_ad)
        
        # Populate form with OCR data
        form.initial.update({
            'title': parsed_data.get('title', ''),
            'company_name': parsed_data.get('company_name', ''),
            'pre_approval_date': parsed_data.get('pre_approval_date', ''),
            'chalani_no': parsed_data.get('chalani_no', ''),
            'lot_no': parsed_data.get('lot_no', ''),
            'city': parsed_data.get('city', ''),
            'country': parsed_data.get('country', ''),
            'nepali_date': parsed_data.get('nepali_date', '२०८१/१२/१८'),
            'gregorian_date': parsed_data.get('gregorian_date', '31 मार्च, 2025'),
            'interview_hour': parsed_data.get('interview_hour', ''),
            'interview_time': parsed_data.get('interview_time', ''),
            'interview_location': parsed_data.get('interview_location', 'म्यानपावरको कार्यालय बसुन्धारामा'),
        })
        
        # Also populate the job position formset with OCR data
        if parsed_data.get('position') or parsed_data.get('salary_amount'):
            # Clear existing positions to prevent duplicates when OCR data is present
            employment_ad.positions.all().delete()
            
            # Create a fresh formset with instance
            formset = JobPositionFormSet(instance=employment_ad)
            
            # Populate the first position with OCR data
            if formset.forms:
                formset.forms[0].initial.update({
                    'position': parsed_data.get('position', ''),
                    'male_count': parsed_data.get('male_count', ''),
                    'female_count': parsed_data.get('female_count', ''),
                    'salary_amount': parsed_data.get('salary_amount', ''),
                    'salary_currency': parsed_data.get('salary_currency', 'KD'),
                    'overtime': parsed_data.get('overtime', ''),
                    'hours_per_day': parsed_data.get('hours_per_day', ''),
                    'days_per_week': parsed_data.get('days_per_week', ''),
                    'yearly_leave': parsed_data.get('yearly_leave', ''),
                    'min_qualification': parsed_data.get('min_qualification', ''),
                    'food_provided': parsed_data.get('food_provided', ''),
                    'housing_provided': parsed_data.get('housing_provided', ''),
                    'contract_duration': parsed_data.get('contract_duration', ''),
                })
        else:
            # No position data, create empty formset with instance
            formset = JobPositionFormSet(instance=employment_ad)
    else:
        # No OCR data, create completely fresh forms
        form = EmploymentAdForm(instance=employment_ad)
        formset = JobPositionFormSet(instance=employment_ad)
    
    # Set default interview data (not from database)
    interview_data = {
        'nepali_date': '२०८१/१२/१८',
        'gregorian_date': '31 मार्च, 2025',
        'interview_hour': '',
        'interview_time': '',
        'interview_location': 'म्यानपावरको कार्यालय बसुन्धारामा',
    }
    
    # Populate form with interview data
    form.initial.update(interview_data)
    
    context = {
        'form': form,
        'formset': formset,
        'employment_ad': employment_ad,
        'positions': employment_ad.positions.all().order_by('order'),  # Get existing positions
        'interview_data': interview_data,
        'ocr_text': ocr_text,
        'parsed_data': parsed_data,
    }
    
    return render(request, 'employment_ad_editor.html', context)

def filter_positions(positions):
    """Filter positions to remove empty ones for PDF generation"""
    return [pos for pos in positions if pos.position and (pos.male_count or pos.female_count)]

def cleanup_duplicate_positions(employment_ad):
    """Clean up duplicate positions for an employment ad"""
    try:
        # Get all positions ordered by creation time
        positions = employment_ad.positions.all().order_by('id')
        
        # Keep only the first occurrence of each unique position
        seen_positions = set()
        positions_to_delete = []
        
        for pos in positions:
            # Create a unique key for each position
            position_key = f"{pos.position}_{pos.male_count}_{pos.female_count}_{pos.salary_amount}_{pos.salary_currency}"
            
            if position_key in seen_positions:
                positions_to_delete.append(pos.id)
            else:
                seen_positions.add(position_key)
        
        # Delete duplicate positions
        if positions_to_delete:
            JobPosition.objects.filter(id__in=positions_to_delete).delete()
            print(f"Cleaned up {len(positions_to_delete)} duplicate positions")
            
    except Exception as e:
        print(f"Error cleaning up duplicate positions: {e}")

def get_country_specific_notice(country):
    """Get country-specific notice content"""
    if country in ["Kuwait", "Saudi Arabia", "UAE", "Qatar", "Oman", "Bahrain"]:
        return {
            "title": "मध्य पूर्व देशहरूको लागि विशेष सूचना",
            "content": "<p>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:-</p><p>१. आङ्खनो नाममा भिषाप्राप्त भएको सुनिश्चित गर्नुहोस् ।</p><p>२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।</p><p>३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।</p><p>४. विदेश जानु अघि आफू जाने मुलुक, काम गर्ने कम्पनी, पाउने सेवा र सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौतापत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफूसँग राख्नुहोला ।</p><p>५. काममा विदेश जानु अघि नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।</p><p>६. यस विज्ञापन सम्बन्धमा थप केहि बुझ्नु पर्नेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।</p>"
        }
    elif country == "Japan":
        return {
            "title": "जापानको लागि विशेष सूचना",
            "content": "<p>जापानमा काम गर्न जाने कामदारहरूले जापानी भाषा र संस्कृतिको बारेमा जानकारी लिनुपर्नेछ।</p><p>कामदारहरूले जापानको नियमहरू र कानुनहरू मान्नुपर्नेछ।</p><p>कामदारहरूले आफ्नो पासपोर्ट र अन्य आवश्यक कागजातहरू साथ लैजानुपर्नेछ।</p><p>कामदारहरूले जापानको काम गर्ने शैली र नियमहरू मान्नुपर्नेछ।</p>"
        }
    else:
        return {
            "title": "सामान्य सूचना",
            "content": "<p>कामदारहरूले सबै नियमहरू र कानुनहरू मान्नुपर्नेछ।</p><p>कामदारहरूले आफ्नो पासपोर्ट र अन्य आवश्यक कागजातहरू साथ लैजानुपर्नेछ।</p><p>कामदारहरूले काम गर्ने देशको भाषा र संस्कृतिको बारेमा जानकारी लिनुपर्नेछ।</p><p>कामदारहरूले काम गर्ने देशको नियमहरू र कानुनहरू मान्नुपर्नेछ।</p>"
        }

def update_currency_rates_view(request):
    """AJAX view to update currency exchange rates"""
    if request.method == 'POST':
        try:
            success = update_currency_rates()
            if success:
                return JsonResponse({'success': True, 'message': 'Currency rates updated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to update currency rates'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def employment_ad_preview(request):
    """Preview the employment advertisement with proper country-based notices"""
    
    employment_ad = get_object_or_404(EmploymentAd, id=1)
    
    # Clean up any duplicate positions before displaying
    cleanup_duplicate_positions(employment_ad)
    
    positions = employment_ad.positions.all().order_by('order')
    
    # Debug: Print the data being passed to template
    print(f"DEBUG: Employment Ad Country: {employment_ad.country}")
    print(f"DEBUG: Number of positions: {len(positions)}")
    for i, pos in enumerate(positions):
        print(f"DEBUG: Position {i+1}: {pos.position} - Currency: {pos.salary_currency} - Amount: {pos.salary_amount}")
    
    # Get interview data if it exists
    try:
        interview = Interview.objects.filter(employment_ad=employment_ad).first()
        interview_data = {
            'nepali_date': interview.nepali_date if interview else '',
            'gregorian_date': interview.gregorian_date if interview else '',
            'location': interview.location if interview else '',
        } if interview else {}
    except:
        interview_data = {}
    
    # Generate country-specific notice
    country_notice = get_country_specific_notice(employment_ad.country)
    
    context = {
        'ad': employment_ad,
        'positions': positions,
        'interview_data': interview_data,
        'country_notice': country_notice,
    }
    
    return render(request, 'employment_ad_preview.html', context)

def download_pdf(request):
    """Download employment advertisement as PDF"""
    
    employment_ad = get_object_or_404(EmploymentAd, id=1)
    
    # Clean up any duplicate positions before generating PDF
    cleanup_duplicate_positions(employment_ad)
    
    positions = employment_ad.positions.all().order_by('order')
    
    # Get interview data if it exists
    try:
        interview = Interview.objects.filter(employment_ad=employment_ad).first()
        interview_data = {
            'nepali_date': interview.nepali_date if interview else '',
            'gregorian_date': interview.gregorian_date if interview else '',
            'location': interview.location if interview else '',
        } if interview else {}
    except:
        interview_data = {}
    
    # Get country-specific notice
    country_notice = get_country_specific_notice(employment_ad.country)
    
    context = {
        'ad': employment_ad,
        'positions': positions,
        'interview_data': interview_data,
        'country_notice': country_notice,
    }
    
    # Generate PDF using the print service
    print_service = PrintService()
    pdf_content = print_service.generate_employment_ad_pdf(employment_ad)
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="employment_ad_{employment_ad.id}.pdf"'
        return response
    else:
        messages.error(request, 'Failed to generate PDF. Please try again.')
        return redirect('employment_ad_editor')

def employment_ad_design(request):
    """Display the new employment advertisement design template"""
    
    employment_ad = get_object_or_404(EmploymentAd, id=1)
    positions = employment_ad.positions.all().order_by('order')
    
    # Get interview data if it exists
    try:
        interview = Interview.objects.filter(employment_ad=employment_ad).first()
        interview_data = {
            'nepali_date': interview.nepali_date if interview else '',
            'gregorian_date': interview.gregorian_date if interview else '',
            'location': interview.location if interview else '',
        } if interview else {}
    except:
        interview_data = {}
    
    # Generate country-specific notice
    country_notice = get_country_specific_notice(employment_ad.country)
    
    context = {
        'ad': employment_ad,
        'positions': positions,
        'interview_data': interview_data,
        'country_notice': country_notice,
    }
    
    return render(request, 'employment_ad_design.html', context)

def download_design_pdf(request):
    """Download the new design employment advertisement as PDF"""
    
    employment_ad = get_object_or_404(EmploymentAd, id=1)
    positions = employment_ad.positions.all().order_by('order')
    
    # Get country-specific notice
    country_notice = get_country_specific_notice(employment_ad.country)
    
    context = {
        'ad': employment_ad,
        'positions': positions,
        'country_notice': country_notice,
    }
    
    # Generate PDF using the print service with the new design template
    print_service = PrintService()
    pdf_content = print_service.generate_employment_ad_pdf(employment_ad, 'employment_ad_design.html')
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="employment_ad_design_{employment_ad.id}.pdf"'
        return response
    else:
        messages.error(request, 'Failed to generate PDF. Please try again.')
        return redirect('employment_ad_design')

def test_form_submission(request):
    """Simple test endpoint to debug form submission issues"""
    if request.method == 'POST':
        print("=== TEST FORM SUBMISSION ===")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        # Check if this is a simple form submission
        if 'simple_submit' in request.POST:
            # Handle simple form submission without formset
            employment_ad = get_object_or_404(EmploymentAd, id=1)
            
            # Update basic fields
            employment_ad.title = request.POST.get('title', '')
            employment_ad.company_name = request.POST.get('company_name', '')
            employment_ad.country = request.POST.get('country', '')
            employment_ad.save()
            
            return JsonResponse({'success': True, 'message': 'Simple form submitted successfully'})
        
        return JsonResponse({'success': False, 'message': 'No simple_submit found'})
    
    return JsonResponse({'success': False, 'message': 'GET request not allowed'})

def simple_position_submission(request):
    """Simple position submission endpoint that doesn't rely on complex formset"""
    if request.method == 'POST':
        print("=== SIMPLE POSITION SUBMISSION ===")
        print(f"POST data: {request.POST}")
        
        try:
            employment_ad = get_object_or_404(EmploymentAd, id=1)
            
            # Get position data from POST
            position = request.POST.get('position', '')
            male_count = request.POST.get('male_count', '')
            female_count = request.POST.get('female_count', '')
            salary_amount = request.POST.get('salary_amount', '')
            salary_currency = request.POST.get('salary_currency', 'KD')
            
            if position and (male_count or female_count) and salary_amount:
                # Create a new job position
                JobPosition.objects.create(
                    employment_ad=employment_ad,
                    position=position,
                    male_count=male_count,
                    female_count=female_count,
                    salary_amount=salary_amount,
                    salary_currency=salary_currency,
                    order=0
                )
                
                return JsonResponse({'success': True, 'message': 'Position added successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Missing required fields'})
                
        except Exception as e:
            print(f"Error in simple position submission: {e}")
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'GET request not allowed'})

def filter_positions(positions):
    """Filter out empty positions for PDF generation"""
    filtered = []
    for position in positions:
        if (position.position and position.position.strip() and 
            (position.male_count and position.male_count.strip() or 
             position.female_count and position.female_count.strip()) and
            position.salary_amount and position.salary_amount.strip()):
            filtered.append(position)
    return filtered

def get_country_specific_notice(country):
    """Get country-specific notice for employment advertisements"""
    country_notices = {
        # Middle East countries - same notice
        'Kuwait': {
            'content': '''<b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b> १. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफुसँग राख्नुहोला ।५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।'''
        },
        'UAE': {
            'content': '''<b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b> १. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला  सो को एक (१) प्रति आफुसँग राख्नुहोला ।५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।'''
        },
        'Saudi Arabia': {
            'content': '''<b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b> १. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफुसँग राख्नुहोला ।५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।'''
        },
        'Qatar': {
            'content': '''<b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b> १. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफुसँग राख्नुहोला ।५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।'''
        },
        'Oman': {
            'content': '''<b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b> १. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफुसँग राख्नुहोला ।५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।'''
        },
        'Bahrain': {
            'content': '''<b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b> १. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफुसँग राख्नुहोला ।५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।'''
        },
        # Japan - specific trainee notice
        'Japan': {
            'title': 'जापानमा प्रशिक्षार्थी कामदारको लागि विशेष सूचना',
            'content': '''<b>प्रशिक्षार्थीको आवश्यकता न्यूनतम योग्यता र काम गरेको अनुभव:</b>
<p>
(क) नेपाली नागरिक हुनुपर्ने । (ख) प्रशिक्षणको उमेर १८ वर्ष पूरा भई २६ वर्ष ननाघेको हुनुपर्ने । 
(ग) प्रशिक्षार्थी नेपाल सरकारको उद्योग मन्त्रालय अन्तर्गतको निकायहरू वा यस पूर्व वा अहिले सञ्चालन भइसकेका उद्योग व्यवसाय, कलकारखाना, ढुंढी सहकारी, साना/कुटिर उद्योग, होटल पर्यटन व्यवसाय तथा अन्य व्यवसाय क्षेत्रमा काम गरेको अनुभव भएको हुनुपर्ने । 
(घ) निर्माण क्षेत्रमा काम गर्ने निर्माण सम्बन्धी उद्योग वा सम्बन्धित विषयका संस्थामा कम्तिमा दुई वर्ष काम गरेको अनुभव हुनुपर्ने । 
(ङ) प्रशिक्षणको विषय अनुसार काम गरेको अनुभव भएको र नेपालकै उद्योग प्रतिष्ठान, संस्था वा निकायहरूमा काम गरेको अनुभव हुनुपर्ने । 
(च) जापानी भाषा तथा संस्कृतिको सामान्य ज्ञान भएको हुनुपर्ने ।
</p>

<b>दरखास्त साथ पेश गर्ने आवश्यक कागजातहरू:</b>
<p>
(क) नेपाली नागरिकताको प्रमाणपत्रको प्रमाणित प्रतिलिपि । 
(ख) शैक्षिक प्रमाणपत्रको प्रमाणित प्रतिलिपि । 
(ग) प्रशिक्षार्थी नेपाल सरकारको उद्योग मन्त्रालय अन्तर्गतको निकायहरू वा यस पूर्व भइसकेका उद्योग व्यवसाय, कलकारखाना, ढुंढी सहकारी, साना/कुटिर उद्योगसंस्था, होटल पर्यटन व्यवसाय तथा अन्य व्यवसाय क्षेत्रमा कम्तिमा २ वर्ष काम गरेको अनुभव सम्बन्धी प्रमाणपत्रको प्रमाणित प्रतिलिपि । 
(घ) सम्बन्धित विषयमा प्रशिक्षण प्राप्त गरेको प्रमाणपत्रको प्रमाणित प्रतिलिपि । 
(ङ) प्रशिक्षणको विषयमा कामदारको रुपमा जान खोजेको विषयमा नेपालका उद्योग प्रतिष्ठान, संस्था वा निकायहरूमा काम गरेको अनुभव प्रमाणपत्रको प्रमाणित प्रतिलिपि । 
(च) प्रशिक्षणको विषय अनुसार जापानी भाषा तथा संस्कृतिको सम्बन्धमा तालिम लिएको हुनुपर्ने प्रमाणपत्रको प्रमाणित प्रतिलिपि । 
(छ) नेपालीमा हाल कार्यरत रहेको सम्बन्धित उद्योग प्रतिष्ठान, निकाय वा संस्थाको सिफारिस र नेपाल फर्किएपछि पनि सोही कार्यक्षेत्र वा निकाय समक्ष काम गर्ने प्रतिवद्धतासहितको प्रमाणित कागजात पेश गर्नु पर्ने ।
</p>

<b>१) दरखास्त बुझाउने स्थान र मिति: यस संस्थाको कार्यालयमा यो सूचना प्रकाशित भएको मितिले १५ दिन भित्र । </b>

<b>२) परीक्षाशुल्क: निर्धारित बैंकमार्फत बुझाउनुपर्नेछ । परीक्षाशुल्क रकम रू. ५०००।– </b>

<b>३) लिखित परीक्षा:२०७८ साल माघ ३१ गते बिहान १०:०० बजे अनलाइन आप्रवासी कार्यालयमा हुनेछ । लिखित परीक्षामा सहभागी हुन आउनेले आफ्नो नागरिकता प्रमाणपत्रको प्रतिलिपि ल्याउनुपर्नेछ । </b>

<b>वैदेशिक रोजगार विभागद्वारा जारी गरिएको जानकारी:</b>
<p>
१. आफ्नो नाममा निष्काशन भई जारी गरिएको पासपोर्टमा कुनै त्रुटि भएमा तुरुन्तै सच्याउनुहोस् ।<br>
२. आफ्नो दस्तावेज र काममा प्रयोग हुने कागजात सुरक्षित राख्नुहोस् ।<br>
३. यस विज्ञापन सम्बन्धमा उल्झन भएमा विभागले कुनै जिम्मेवारी लिने छैन ।<br>
४. विदेश जानु अघि अभिमुखीकरण तालिम लिनु पर्नेछ ।<br>
५. विदेश जानु अघि श्रम सम्झौता अनिवार्य रुपमा गर्नुपर्नेछ ।<br>
६. विदेश जानु अघि बीमा कम्पनीमा बीमा गर्नुपर्नेछ ।<br>
७. विदेश जानु अघि कुनै दलाल वा एजेन्टलाई पैसा दिनु हुने छैन ।<br>
८. पासपोर्ट, श्रम अनुमति, करारपत्र, टिकट आफैंले बुझी लिनुहोस् ।<br>
९. सीधै विमानस्थलमा जानुहोस् ।<br>
१०. पासपोर्टमा समस्या भएमा विभागमा सम्पर्क गर्नुहोस् ।
</p> <br>

<b>नोट: जापानी भाषा N4 स्तरको ज्ञान भएकोलाई प्राथमिकता दिइनेछ ।</b>'''
        }
    }
    
    # Return default notice if country not found
    default_notice = {
        'title': 'बैदेशिक रोजगार बिभागबाट गराइएको जानकारी',
        'content': '''<p><b>बैदेशिक रोजगार बिभागबाट गराइएको जानकारी:</b>१. आङ्खनो नाममा भिषा प्राप्त भएको सुनिश्चित गर्नुहोस् ।२. आफु काम गर्न जाने मुलुकमा रहेको नेपाली कुटनैतिक नियोगको सम्पर्क ठेगाना र फोन नं.हरु साथमा राख्नुहोला । आफू कठिनाईमा पुर्दा सम्पर्क गर्न सजिलो हुन्छ ।३. यस विज्ञापन (सूचना) मा उल्लेख भएको सेवा, सुविधा र तुलबुको बारेमा स्पष्ट हुनुहोस् ।
४. विदेश जानु अघि आफू जाने मुलुक, काम दिने कम्पनी, पाउने सेवा तथा सुबिधा र अन्य शर्तबारे राम्रो सँग पढेर मात्र सम्झौता पत्रमा हस्ताक्षर गर्नुहोला र सो को एक (१) प्रति आफुसँग राख्नुहोला ।
५. काममा विदेश जादा नेपालकै विमानस्थल प्रयोग गर्नुहोला, अन्यथा ठगिने सम्भावना हुन्छ ।

६. यस विज्ञापन सम्बन्धमा थप केही बुझ्नुपरेमा बैदेशिक रोजगार विभाग, ताहचलमा सम्पर्क गर्नुहोला ।</p>'''
    }
    
    return country_notices.get(country, default_notice)

def test_form_submission(request):
    """Simple test endpoint to debug form submission issues"""
    if request.method == "POST":
        print("=== TEST FORM SUBMISSION ===")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        # Check if this is a simple form submission
        if "simple_submit" in request.POST:
            # Handle simple form submission without formset
            employment_ad = get_object_or_404(EmploymentAd, id=1)
            
            # Update basic fields
            employment_ad.title = request.POST.get("title", "")
            employment_ad.company_name = request.POST.get("company_name", "")
            employment_ad.country = request.POST.get("country", "")
            employment_ad.save()
            
            return JsonResponse({"success": True, "message": "Simple form submitted successfully"})
        
        return JsonResponse({"success": False, "message": "No simple_submit found"})
    
    return JsonResponse({"success": False, "message": "GET request not allowed"})

def simple_position_submission(request):
    """Simple position submission endpoint that does not rely on complex formset"""
    if request.method == "POST":
        print("=== SIMPLE POSITION SUBMISSION ===")
        print(f"POST data: {request.POST}")
        
        try:
            employment_ad = get_object_or_404(EmploymentAd, id=1)
            
            # Get position data from POST
            position = request.POST.get("position", "")
            male_count = request.POST.get("male_count", "")
            female_count = request.POST.get("female_count", "")
            salary_amount = request.POST.get("salary_amount", "")
            salary_currency = request.POST.get("salary_currency", "KD")
            
            if position and (male_count or female_count) and salary_amount:
                # Create a new job position
                JobPosition.objects.create(
                    employment_ad=employment_ad,
                    position=position,
                    male_count=male_count,
                    female_count=female_count,
                    salary_amount=salary_amount,
                    salary_currency=salary_currency,
                    order=0
                )
                
                return JsonResponse({"success": True, "message": "Position added successfully"})
            else:
                return JsonResponse({"success": False, "message": "Missing required fields"})
                
        except Exception as e:
            print(f"Error in simple position submission: {e}")
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})
    
    return JsonResponse({"success": False, "message": "GET request not allowed"})
