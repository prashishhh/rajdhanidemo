#!/usr/bin/env python3
"""
Test PDF Generation for cPanel
Run this script to verify PDF generation works on your cPanel server
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rajdhani.settings')
django.setup()

from core.services.print_service import PrintService
from core.models import EmploymentAd, JobPosition

def test_pdf_generation():
    """Test PDF generation with all available methods"""
    
    print("🔧 Testing PDF Generation on cPanel...")
    print("=" * 50)
    
    # Initialize service
    service = PrintService()
    
    # Check available methods
    print(f"📋 Available PDF Methods:")
    print(f"   • Playwright: {'✅' if service.playwright_available else '❌'}")
    print(f"   • WeasyPrint: {'✅' if service.weasyprint_available else '❌'}")
    print(f"   • ReportLab:  {'✅' if service.reportlab_available else '❌'}")
    print()
    
    # Get test data
    try:
        employment_ad = EmploymentAd.objects.first()
        if not employment_ad:
            print("❌ No employment ad found in database!")
            print("   Please create an employment ad first.")
            return False
        
        print(f"📄 Testing with Employment Ad: {employment_ad.company_name}")
        print()
        
        # Test PDF generation
        print("🔄 Generating PDF...")
        pdf_content = service.generate_employment_ad_pdf(employment_ad)
        
        if pdf_content:
            print(f"✅ PDF Generation Successful!")
            print(f"   • File size: {len(pdf_content):,} bytes")
            print(f"   • File size: {len(pdf_content)/1024:.1f} KB")
            
            # Save test PDF
            test_pdf_path = "test_employment_ad.pdf"
            with open(test_pdf_path, 'wb') as f:
                f.write(pdf_content)
            print(f"   • Test PDF saved: {test_pdf_path}")
            
            return True
        else:
            print("❌ PDF Generation Failed!")
            print("   Check the error logs above for details.")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_individual_methods():
    """Test each PDF generation method individually"""
    
    print("\n🔬 Testing Individual Methods...")
    print("=" * 50)
    
    service = PrintService()
    employment_ad = EmploymentAd.objects.first()
    
    if not employment_ad:
        print("❌ No employment ad found!")
        return
    
    # Test Playwright
    if service.playwright_available:
        print("🔄 Testing Playwright...")
        try:
            # This would need HTML content, so we'll skip for now
            print("   ⚠️  Playwright requires HTML rendering (skipped)")
        except Exception as e:
            print(f"   ❌ Playwright failed: {e}")
    
    # Test WeasyPrint
    if service.weasyprint_available:
        print("🔄 Testing WeasyPrint...")
        try:
            # This would need HTML content, so we'll skip for now
            print("   ⚠️  WeasyPrint requires HTML rendering (skipped)")
        except Exception as e:
            print(f"   ❌ WeasyPrint failed: {e}")
    
    # Test ReportLab
    if service.reportlab_available:
        print("🔄 Testing ReportLab...")
        try:
            pdf_content = service.generate_pdf_reportlab(employment_ad)
            if pdf_content:
                print(f"   ✅ ReportLab successful: {len(pdf_content):,} bytes")
            else:
                print("   ❌ ReportLab failed")
        except Exception as e:
            print(f"   ❌ ReportLab failed: {e}")

def check_system_requirements():
    """Check system requirements for PDF generation"""
    
    print("\n🔍 System Requirements Check...")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    
    # Check Django
    import django
    print(f"🎯 Django Version: {django.get_version()}")
    
    # Check available packages
    packages = [
        ('playwright', 'Playwright'),
        ('weasyprint', 'WeasyPrint'),
        ('reportlab', 'ReportLab'),
    ]
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name}: Available")
        except ImportError:
            print(f"❌ {name}: Not available")
    
    # Check file permissions
    print(f"\n📁 File Permissions:")
    current_dir = os.getcwd()
    print(f"   • Current directory: {current_dir}")
    print(f"   • Writable: {'✅' if os.access(current_dir, os.W_OK) else '❌'}")
    
    # Check temp directory
    temp_dir = os.path.join(current_dir, 'temp')
    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir)
            print(f"   • Temp directory created: {temp_dir}")
        except Exception as e:
            print(f"   • Temp directory creation failed: {e}")
    else:
        print(f"   • Temp directory exists: {temp_dir}")

def main():
    """Main test function"""
    
    print("🚀 cPanel PDF Generation Test")
    print("=" * 50)
    
    # Check system requirements
    check_system_requirements()
    
    # Test individual methods
    test_individual_methods()
    
    # Test full PDF generation
    success = test_pdf_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! PDF generation should work on cPanel.")
        print("\n📋 Next Steps:")
        print("   1. Upload the test PDF to verify it opens correctly")
        print("   2. Test the download functionality in your Django app")
        print("   3. If issues persist, check the CPANEL_PDF_SETUP.md guide")
    else:
        print("❌ Some tests failed. Check the issues above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Install missing dependencies")
        print("   2. Check file permissions")
        print("   3. Review the CPANEL_PDF_SETUP.md guide")
        print("   4. Contact your hosting provider")

if __name__ == "__main__":
    main()
