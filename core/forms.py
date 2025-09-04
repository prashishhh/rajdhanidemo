from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import News, EmploymentAd, JobPosition, Interview, CurrencyRate


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


# Custom formset for job positions that handles new records properly
class JobPositionFormSet(BaseInlineFormSet):
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

class EmploymentAdForm(forms.ModelForm):
    """Form for employment advertisement main information"""
    
    # Override title field to make it optional
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'जापानमा रोजगारी'
        })
    )
    
    # Add interview fields as form fields (not model fields)
    interview_nepali_date = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '२०८२/०५/११'
        })
    )
    interview_gregorian_date = forms.CharField(
        max_length=50, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '30 August, 2025'
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
            'class': 'form-control',
            'placeholder': 'म्यानपावरको कार्यालय बसुन्धारामा'
        })
    )
    
    class Meta:
        model = EmploymentAd
        fields = [
            'title', 'company_name', 'country', 'pre_approval_date', 'chalani_no', 
            'lot_no', 'city',
            'medical_cost_local', 'medical_cost_foreign', 'insurance_local', 'insurance_employment',
            'air_ticket', 'visa_fee', 'visa_stamp_fee', 'recruitment_fee', 'welfare_fund',
            'labor_fee', 'service_fee', 'extra_notes', 'interview_custom_text',
            # Company Banner Fields
            'company_logo_text', 'company_logo_image', 'company_banner_title', 'company_address', 'company_phone',
            'company_email', 'company_website', 'license_number'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'FINE FARE FOOD MARKET L.L.C'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kuwait, UAE, Japan, etc. (देश अनुसार स्वचालित सूचना देखिनेछ)'
            }),
            'pre_approval_date': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '2025-08-22'
            }),
            'chalani_no': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '६०२३७४३२'
            }),
            'lot_no': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '३२२८६२'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'West Abu'
            }),
            # Extra Information fields with payment options
            'medical_cost_local': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'medical_cost_foreign': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'insurance_local': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'insurance_employment': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'air_ticket': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले दिने', 'रोजगारदाताले दिने')
            ]),
            'visa_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'visa_stamp_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'recruitment_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'welfare_fund': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'रु. ७०० /-'
            }),
            'labor_fee': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'कामदारले तिर्ने रु. १५०० /-'
            }),
            'service_fee': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('कामदारले तिर्ने', 'कामदारले तिर्ने'),
                ('रोजगारदाताले व्यहोर्ने', 'रोजगारदाताले व्यहोर्ने')
            ]),
            'extra_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'यहाँ आफ्नो विशेष सूचना लेख्नुहोस् (यदि कुनै छ भने)'
            }),
            # Company Banner Widgets
            'company_logo_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'LOGO'
            }),
            'company_logo_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'logo-upload'
            }),
            'company_banner_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'BEST EMPLOYMENT HR SOLUTION'
            }),
            'company_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ठेगाना: Kathmandu-9, Gaushala, Nepal.'
            }),
            'company_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'फोन: +977-1-5922788'
            }),
            'company_email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'इमेल: info@besthr.com.np, bestemploymenthr123@gmail.com'
            }),
            'company_website': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'वेब: www.besthr.com.np'
            }),
            'license_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gov. Lic. Number 1714/081/082'
            }),
            'interview_custom_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'यहाँ आफ्नो विशेष अन्तरवार्ता सूचना लेख्नुहोस् (खाली छोड्नुहोस् यदि स्वचालित ८ दिन गणना चाहनुहुन्छ भने)'
            }),
        }

class JobPositionForm(forms.ModelForm):
    """Form for individual job positions"""
    
    class Meta:
        model = JobPosition
        fields = [
            'position', 'male_count', 'female_count', 'salary_amount', 'salary_currency', 'salary_npr',
            'overtime', 'hours_per_day', 'days_per_week', 'yearly_leave',
            'min_qualification', 'food_provided', 'housing_provided', 'contract_duration', 'order'
        ]
        widgets = {
            'position': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'BAKERY WORKER'
            }),
            'male_count': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'संख्या भर्नुहोस्'
            }),
            'female_count': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'संख्या भर्नुहोस्'
            }),
            'salary_amount': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '140'
            }),
            'salary_currency': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
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
                'placeholder': '५२,९९२/-',
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
            'hours_per_day': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'घण्टा भर्नुहोस्'
            }),
            'days_per_week': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'दिन भर्नुहोस्'
            }),
            'yearly_leave': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('छ', 'छ'), 
                ('छैन', 'छैन'),
                ('कम्पनीको नियमानुसार', 'कम्पनीको नियमानुसार')
            ]),
            'min_qualification': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'छान्नुहोस्'),
                ('कम्तिमा पनि निम्नलिखित मुख्य', 'कम्तिमा पनि निम्नलिखित मुख्य'),
                ('+2', '+2'),
                ('SEE', 'SEE'),
                ('Bachelors', 'Bachelors'),
                ('सम्बन्धित काममा दक्ष', 'सम्बन्धित काममा दक्ष')
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
            'contract_duration': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'अवधि भर्नुहोस्'
            }),
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

