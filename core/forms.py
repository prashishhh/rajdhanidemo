from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import News, EmploymentAd, JobPosition, Interview, CurrencyRate
from .mixins import ProductionSafeForm, ProductionSafeFormset


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# Custom formset for job positions that handles new records properly
class JobPositionFormSet(ProductionSafeFormset, BaseInlineFormSet):
    """Custom formset for job positions that handles new positions properly"""
    
    def clean(self):
        """Custom validation for the formset"""
        cleaned_data = super().clean()
        # Additional validation if needed
        return cleaned_data
    
    def save_new(self, form, commit=True):
        """Override to handle new position creation"""
        instance = super().save_new(form, commit=False)
        # Set any additional fields if needed
        return instance


from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'News Title'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Write your news story here...', 'rows': 7}),
        }

from .models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'description', 'meeting_time', 'meeting_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Meeting Title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Description', 'rows': 3}),
            'meeting_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://... (optional)'}),
        }

class InterviewForm(forms.ModelForm):
    """Form for individual interview details"""
    
    class Meta:
        model = Interview
        fields = [
            'interview_type', 'nepali_date', 'gregorian_date', 'time', 'location', 'template'
        ]
        widgets = {
            'interview_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'अन्तर्वार्ता'
            }),
            'nepali_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '२०८१/१२/१८'
            }),
            'gregorian_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '31 मार्च, 2025'
            }),
            'time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'बिहान 11 बजे'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'म्यानपावरको कार्यालय बसुन्धारामा'
            }),
            'template': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'अन्तर्वार्ता: मिति {nepali_date} गते ({gregorian_date}) {time} {location} हुनेछ।'
            }),
        }

class EmploymentAdForm(ProductionSafeForm):
    """Form for employment advertisement main information"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for select fields - always set defaults
        # This will show defaults every time the form loads
        self.fields['medical_cost_local'].initial = 'कामदारले तिर्ने'
        self.fields['medical_cost_foreign'].initial = 'रोजगारदाताले व्यहोर्ने'
        self.fields['insurance_local'].initial = 'कामदारले तिर्ने'
        self.fields['insurance_employment'].initial = 'बिमा हुने र प्रिमियम रोजगारदाताले व्यहोर्ने'
        self.fields['air_ticket'].initial = 'रोजगारदाताले दिने'
        self.fields['visa_fee'].initial = 'रोजगारदाताले व्यहोर्ने'
        self.fields['visa_stamp_fee'].initial = 'रोजगारदाताले व्यहोर्ने'
        self.fields['recruitment_fee'].initial = 'रू.७००/- कामदारले व्यहोर्ने'
        self.fields['service_fee'].initial = 'नि:शुल्क'
        
        # Set default values for text fields
        self.fields['welfare_fund'].initial = 'रू.२३०८/- कामदारले व्यहोर्ने'
        self.fields['labor_fee'].initial = 'रू.१५००/- कामदारले व्यहोर्ने'
    
    # Override title field to make it optional
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Add interview fields as form fields (not model fields)
    interview_nepali_date = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    interview_gregorian_date = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    interview_hour = forms.ChoiceField(
        required=False,
        choices=[('', 'छान्नुहोस्')] + [(str(i), str(i)) for i in range(1, 13)],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    interview_time = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'छान्नुहोस्'),
            ('बिहान', 'बिहान'),
            ('दिउँसो', 'दिउँसो'),
            ('बेलुकी', 'बेलुकी'),
            ('राति', 'राति')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    interview_location = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Add clear field for banner image
    company_banner_image_clear = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    # Override company banner fields to make them optional
    company_banner_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    company_address = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    company_phone = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    company_email = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    company_website = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    license_number = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    def clean_company_banner_title(self):
        """Validate company banner title"""
        title = self.cleaned_data.get('company_banner_title', '').strip()
        if title and len(title) > 200:
            raise forms.ValidationError('कम्पनीको नाम २०० अक्षर भन्दा लामो हुनुहुँदैन।')
        return title
    
    def clean_company_address(self):
        """Validate company address"""
        address = self.cleaned_data.get('company_address', '').strip()
        if address and len(address) > 300:
            raise forms.ValidationError('ठेगाना ३०० अक्षर भन्दा लामो हुनुहुँदैन।')
        return address
    
    def clean_company_phone(self):
        """Validate company phone"""
        phone = self.cleaned_data.get('company_phone', '').strip()
        if phone and len(phone) > 100:
            raise forms.ValidationError('फोन नम्बर १०० अक्षर भन्दा लामो हुनुहुँदैन।')
        return phone
    
    def clean_company_email(self):
        """Validate company email"""
        email = self.cleaned_data.get('company_email', '').strip()
        if email and len(email) > 200:
            raise forms.ValidationError('इमेल २०० अक्षर भन्दा लामो हुनुहुँदैन।')
        return email
    
    def clean_company_website(self):
        """Validate company website"""
        website = self.cleaned_data.get('company_website', '').strip()
        if website and len(website) > 100:
            raise forms.ValidationError('वेबसाइट १०० अक्षर भन्दा लामो हुनुहुँदैन।')
        return website
    
    def clean_license_number(self):
        """Validate license number"""
        license_num = self.cleaned_data.get('license_number', '').strip()
        if license_num and len(license_num) > 100:
            raise forms.ValidationError('लाइसेन्स नम्बर १०० अक्षर भन्दा लामो हुनुहुँदैन।')
        return license_num
    
    class Meta:
        model = EmploymentAd
        fields = [
            'title', 'company_name', 'right_section_text', 'country', 'pre_approval_date', 'chalani_no', 
            'lot_no', 'city',
            'medical_cost_local', 'medical_cost_foreign', 'insurance_local', 'insurance_employment',
            'air_ticket', 'visa_fee', 'visa_stamp_fee', 'recruitment_fee', 'welfare_fund',
            'labor_fee', 'service_fee', 'extra_notes', 'interview_custom_text',
            # Company Banner Fields
            'company_logo_text', 'company_logo_image', 'company_banner_image', 'company_banner_text', 'company_banner_title', 'company_address', 'company_phone',
            'company_email', 'company_website', 'license_number', 'company_banner_image_clear'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'right_section_text': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'हैन?'),
                ('पुन : विज्ञापन', 'हो?')
            ]),
            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'pre_approval_date': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'chalani_no': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'lot_no': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            # Extra Information fields with payment options
            'medical_cost_local': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'medical_cost_foreign': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'insurance_local': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'insurance_employment': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने'),
                ('बिमा हुने र प्रिमियम रोजगारदाताले व्यहोर्ने', 'बिमा हुने र प्रिमियम रोजगारदाताले व्यहोर्ने')
            ]),
            'air_ticket': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले दिने', 'रोजगारदाताले दिने')
            ]),
            'visa_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'visa_stamp_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'recruitment_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने'),
                ('रू.७००/- कामदारले व्यहोर्ने', 'रू.७००/- कामदारले व्यहोर्ने')
            ]),
            'welfare_fund': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'रू.२३०८/- कामदारले व्यहोर्ने'
            }),
            'labor_fee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'रू.१५००/- कामदारले व्यहोर्ने'
            }),
            'service_fee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'नि:शुल्क'
            }),
            'extra_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            # Company Banner Widgets
            'company_logo_text': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'company_logo_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'logo-upload'
            }),
            'company_banner_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'banner-upload'
            }),
            'company_banner_text': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'interview_custom_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }

class JobPositionForm(ProductionSafeForm):
    """Form for individual job positions"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for job position fields
        self.fields['min_qualification'].initial = 'सम्बन्धित<br>काममा दक्ष'
        self.fields['overtime'].initial = 'कम्पनीको नियमानुसार'
        self.fields['hours_per_day'].initial = '८ घण्टा'
        self.fields['days_per_week'].initial = '६ दिन'
        self.fields['yearly_leave'].initial = 'कम्पनीको नियमानुसार'
        self.fields['contract_duration'].initial = '२ वर्ष'
    
    class Meta:
        model = JobPosition
        fields = [
            'position', 'male_count', 'female_count', 'salary_amount', 'salary_currency', 'salary_npr',
            'overtime', 'hours_per_day', 'days_per_week', 'yearly_leave',
            'min_qualification', 'food_provided', 'housing_provided', 'contract_duration', 'order'
        ]
        widgets = {
            'position': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'male_count': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'female_count': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'salary_amount': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'salary_currency': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('JPY', 'Japanese Yen (¥)'),
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
            ]),
            'salary_npr': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'overtime': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('छ', 'छ'), 
                ('छैन', 'छैन'),
                ('कम्पनीको नियमानुसार', 'कम्पनीको नियमानुसार')
            ]),
            'hours_per_day': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('६ घण्टा', '६ घण्टा'),
                ('७ घण्टा', '७ घण्टा'),
                ('८ घण्टा', '८ घण्टा'),
                ('९ घण्टा', '९ घण्टा'),
                ('१० घण्टा', '१० घण्टा'),
                ('१२ घण्टा', '१२ घण्टा')
            ]),
            'days_per_week': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('५ दिन', '५ दिन'),
                ('६ दिन', '६ दिन'),
                ('७ दिन', '७ दिन')
            ]),
            'yearly_leave': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('छ', 'छ'), 
                ('छैन', 'छैन'),
                ('कम्पनीको नियमानुसार', 'कम्पनीको नियमानुसार'),
                ('२१ दिन', '२१ दिन')
            ]),
            'min_qualification': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('कम्तिमा पनि निम्नलिखित मुख्य', 'कम्तिमा पनि निम्नलिखित मुख्य'),
                ('+2', '+2'),
                ('SEE', 'SEE'),
                ('Bachelors', 'Bachelors'),
                ('सम्बन्धित<br>काममा दक्ष', 'सम्बन्धित\nकाममा दक्ष')
            ]),
            'food_provided': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('छ', 'छ'), 
                ('छैन', 'छैन')
            ]),
            'housing_provided': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('छ', 'छ'), 
                ('छैन', 'छैन')
            ]),
            'contract_duration': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्...'),
                ('१ वर्ष', '१ वर्ष'),
                ('२ वर्ष', '२ वर्ष'),
                ('३ वर्ष', '३ वर्ष'),
                ('४ वर्ष', '४ वर्ष'),
                ('५ वर्ष', '५ वर्ष')
            ]),
            'order': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields not required for new positions
        for field_name, field in self.fields.items():
            if field_name not in ['employment_ad']:  # Only keep foreign key required
                field.required = False
        
        # Handle id field for new records
        if 'id' in self.fields:
            self.fields['id'].required = False
            self.fields['id'].widget = forms.HiddenInput()

# Create the formset for job positions
JobPositionFormSet = inlineformset_factory(
    EmploymentAd, 
    JobPosition, 
    form=JobPositionForm,
    extra=1,  # Start with 1 empty form
    max_num=10,  # Maximum 10 positions
    can_delete=True,  # Allow deletion of positions
    can_order=True,   # Allow reordering
    fields=[
        'position', 'male_count', 'female_count', 'salary_amount', 'salary_currency', 'salary_npr',
        'overtime', 'hours_per_day', 'days_per_week', 'yearly_leave',
        'min_qualification', 'food_provided', 'housing_provided', 'contract_duration', 'order'
    ]
)

# Create the formset for interviews
InterviewFormSet = inlineformset_factory(
    EmploymentAd,
    Interview,
    form=InterviewForm,
    extra=1,  # Start with 1 empty form
    can_delete=True,  # Allow deletion of interviews
    can_order=True,   # Allow reordering
    fields=[
        'interview_type', 'nepali_date', 'gregorian_date', 'time', 'location', 'template'
    ]
)

