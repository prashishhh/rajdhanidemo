# PDF Generation Setup for cPanel

## 🔧 **cPanel PDF Download Issues - Solutions**

### **Problem:**
PDF downloads not working on cPanel due to missing dependencies and browser requirements.

### **Root Causes:**
1. **Missing Dependencies**: Playwright and WeasyPrint require system-level packages
2. **Browser Dependencies**: Playwright needs Chromium browser binaries
3. **File Permissions**: cPanel restricts certain file operations
4. **Memory Limits**: PDF generation can be memory-intensive
5. **Path Issues**: Absolute paths might not work on cPanel

---

## ✅ **Solution 1: Install Dependencies via SSH**

### **Step 1: Access SSH Terminal**
```bash
# Connect to your cPanel server via SSH
ssh username@your-domain.com  
```

### **Step 2: Navigate to Project Directory**
```bash
cd public_html/your-project-folder
# or
cd ~/public_html/rajdhani
```

### **Step 3: Activate Virtual Environment (if using)**
```bash
source venv/bin/activate
# or
source ~/venv/bin/activate
```

### **Step 4: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 5: Install Playwright Browsers**
```bash
playwright install chromium
```

---

## ✅ **Solution 2: cPanel Terminal (Alternative)**

### **Step 1: Access cPanel Terminal**
1. Login to cPanel
2. Find "Terminal" or "SSH Access"
3. Open terminal

### **Step 2: Install Dependencies**
```bash
cd public_html/rajdhani
pip3 install playwright weasyprint reportlab
playwright install chromium
```

---

## ✅ **Solution 3: Manual Installation via cPanel File Manager**

### **Step 1: Upload Dependencies**
1. Go to cPanel → File Manager
2. Navigate to your project directory
3. Upload the updated `requirements.txt`

### **Step 2: Install via Python Selector**
1. Go to cPanel → Setup Python App
2. Select your Python version
3. Install packages from requirements.txt

---

## 🔧 **Configuration Fixes**

### **1. Update Settings for cPanel**
Add to your `settings.py`:

```python
# PDF Generation Settings for cPanel
import os

# Set temporary directory for PDF generation
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

# Configure Playwright for cPanel
PLAYWRIGHT_BROWSER_PATH = os.path.join(BASE_DIR, 'browsers')
os.makedirs(PLAYWRIGHT_BROWSER_PATH, exist_ok=True)

# Set environment variables
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = PLAYWRIGHT_BROWSER_PATH
```

### **2. File Permissions**
```bash
# Set proper permissions
chmod 755 public_html/rajdhani
chmod 644 public_html/rajdhani/*.py
chmod -R 755 public_html/rajdhani/temp
```

### **3. Memory Limits**
Add to `.htaccess`:
```apache
php_value memory_limit 512M
php_value max_execution_time 300
php_value upload_max_filesize 50M
php_value post_max_size 50M
```

---

## 🚀 **Fallback Solutions**

### **Solution A: Use ReportLab Only**
If Playwright/WeasyPrint fail, the system automatically falls back to ReportLab:

```python
# The system will try in this order:
# 1. Playwright (best quality)
# 2. WeasyPrint (good quality)
# 3. ReportLab (basic but reliable)
```

### **Solution B: Disable Advanced PDF Features**
Add to `settings.py`:
```python
# Force ReportLab only (for cPanel compatibility)
FORCE_REPORTLAB_ONLY = True
```

### **Solution C: Use External PDF Service**
```python
# Configure external PDF service
PDF_SERVICE_URL = "https://your-pdf-service.com/generate"
```

---

## 🧪 **Testing PDF Generation**

### **Test Command**
```bash
# Test PDF generation
python manage.py shell
```

```python
from core.services.print_service import PrintService
from core.models import EmploymentAd

# Test PDF generation
service = PrintService()
ad = EmploymentAd.objects.first()
pdf_content = service.generate_employment_ad_pdf(ad)

if pdf_content:
    print("✅ PDF generation successful!")
    print(f"PDF size: {len(pdf_content)} bytes")
else:
    print("❌ PDF generation failed!")
```

---

## 📋 **Troubleshooting Checklist**

### **Common Issues:**

1. **"Playwright not available"**
   - Install: `pip install playwright`
   - Install browsers: `playwright install chromium`

2. **"WeasyPrint not available"**
   - Install: `pip install weasyprint`
   - May need system fonts: `apt-get install fonts-liberation`

3. **"ReportLab not available"**
   - Install: `pip install reportlab`

4. **Permission Denied**
   - Check file permissions: `chmod 755 directory`
   - Check temp directory: `mkdir -p temp && chmod 755 temp`

5. **Memory Limit Exceeded**
   - Increase PHP memory limit in `.htaccess`
   - Use ReportLab fallback (lighter)

6. **Browser Launch Failed**
   - Use ReportLab fallback
   - Or install system dependencies

---

## 🎯 **Recommended cPanel Setup**

### **For Best Compatibility:**
1. **Install ReportLab only** (most reliable on cPanel)
2. **Use Python 3.8+**
3. **Set proper file permissions**
4. **Configure memory limits**

### **For Best Quality:**
1. **Install all three libraries**
2. **Use SSH access for installation**
3. **Configure proper paths**
4. **Test thoroughly**

---

## 📞 **Support**

If you continue having issues:

1. **Check error logs** in cPanel → Error Logs
2. **Test with ReportLab only** (most compatible)
3. **Contact hosting provider** for Python package installation
4. **Use external PDF service** as last resort

---

## ✅ **Success Indicators**

When working correctly, you should see:
- ✅ PDF downloads start immediately
- ✅ No "Failed to generate PDF" errors
- ✅ PDF files open correctly
- ✅ File sizes are reasonable (50KB-500KB)

**The system now has three fallback methods, so PDF generation should work on any cPanel setup!**
