# cPanel PDF Download Fix

## Problem
The PDF download on cPanel shows a simplified layout instead of the exact employment_preview.html template.

## Root Cause
The PDF generation is falling back to ReportLab which creates a basic table layout instead of using the HTML template.

## Solution

### Step 1: Install WeasyPrint on cPanel

**Option A: Via cPanel Terminal**
1. Go to cPanel → Terminal
2. Run these commands:
```bash
cd public_html/rajdhani
pip3 install weasyprint
```

**Option B: Via SSH (if available)**
```bash
ssh username@your-domain.com
cd public_html/rajdhani
pip3 install weasyprint
```

**Option C: Via Python Selector**
1. Go to cPanel → Setup Python App
2. Select your Python version
3. Install package: `weasyprint`

### Step 2: Install System Dependencies (if needed)

WeasyPrint may require system fonts. If you get font errors, install:
```bash
# For Ubuntu/Debian based systems
sudo apt-get install fonts-liberation

# For CentOS/RHEL based systems
sudo yum install liberation-fonts
```

### Step 3: Test PDF Generation

1. Go to your employment ad preview page
2. Click "Download PDF"
3. The PDF should now match the preview exactly

### Step 4: Verify Installation

Check if WeasyPrint is working by running this in Django shell:
```python
python manage.py shell
```

```python
from core.services.print_service import PrintService
from core.models import EmploymentAd

service = PrintService()
print(f"WeasyPrint available: {service.weasyprint_available}")

ad = EmploymentAd.objects.first()
if ad:
    pdf_content = service.generate_employment_ad_pdf(ad)
    if pdf_content:
        print("✅ PDF generation working!")
    else:
        print("❌ PDF generation failed")
```

## Expected Result

After installing WeasyPrint, the PDF download should show:
- ✅ Exact same layout as employment_preview.html
- ✅ Proper fonts (Kalimati, Olympia-BoldCond)
- ✅ Correct styling and formatting
- ✅ All tables and sections as in preview

## Troubleshooting

### If WeasyPrint installation fails:
1. Try installing with `--user` flag: `pip3 install --user weasyprint`
2. Check Python version compatibility
3. Contact your hosting provider for system package installation

### If PDF still shows simplified layout:
1. Check error logs in cPanel
2. Verify WeasyPrint is installed: `python3 -c "import weasyprint"`
3. The system will show warnings in logs about which PDF library is being used

## Alternative Solution

If WeasyPrint cannot be installed, the system will use ReportLab fallback which creates the simplified layout you saw. This is a limitation of the hosting environment.

## Success Indicators

When working correctly, you should see:
- PDF matches the preview exactly
- No "Using ReportLab fallback" warnings in logs
- WeasyPrint available: True in the test above
