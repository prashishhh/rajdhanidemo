"""
Print Service for Employment Advertisements
Uses Playwright to generate high-quality PDFs from HTML previews
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not available. Install with: pip install playwright")

try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger.warning("WeasyPrint not available. Install with: pip install weasyprint")


class PrintService:
    """Service for generating high-quality PDFs from employment ad previews"""
    
    def __init__(self):
        self.playwright_available = PLAYWRIGHT_AVAILABLE
        self.weasyprint_available = WEASYPRINT_AVAILABLE
        
        if not self.playwright_available and not self.weasyprint_available:
            logger.error("No PDF generation library available. Install either Playwright or WeasyPrint.")
    
    def generate_pdf_playwright(self, html_content: str, filename: str = "employment_ad.pdf") -> Optional[bytes]:
        """
        Generate PDF using Playwright (preferred method)
        Returns PDF content as bytes or None if failed
        """
        if not self.playwright_available:
            logger.error("Playwright not available")
            return None
        
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Set content and wait for fonts to load
                page.set_content(html_content, wait_until="networkidle")
                
                # Wait a bit for any dynamic content
                page.wait_for_timeout(1000)
                
                # Generate PDF with specific dimensions and settings
                pdf_content = page.pdf(
                    format="A4",
                    print_background=True,
                    margin={
                        "top": "0.5cm",
                        "right": "0.5cm", 
                        "bottom": "0.5cm",
                        "left": "0.5cm"
                    },
                    scale=1.0,
                    prefer_css_page_size=True
                )
                
                browser.close()
                return pdf_content
                
        except Exception as e:
            logger.error(f"Playwright PDF generation failed: {e}")
            return None
    
    def generate_pdf_weasyprint(self, html_content: str, filename: str = "employment_ad.pdf") -> Optional[bytes]:
        """
        Generate PDF using WeasyPrint (fallback method)
        Returns PDF content as bytes or None if failed
        """
        if not self.weasyprint_available:
            logger.error("WeasyPrint not available")
            return None
        
        try:
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html_path = f.name
            
            try:
                # Generate PDF
                pdf_doc = weasyprint.HTML(filename=temp_html_path)
                pdf_content = pdf_doc.write_pdf()
                return pdf_content
            finally:
                # Clean up temporary file
                os.unlink(temp_html_path)
                
        except Exception as e:
            logger.error(f"WeasyPrint PDF generation failed: {e}")
            return None
    
    def generate_employment_ad_pdf(self, employment_ad, template_name: str = "employment_ad_preview.html") -> Optional[bytes]:
        """
        Generate PDF for employment advertisement
        Args:
            employment_ad: EmploymentAd model instance
            template_name: Template to use for rendering
        Returns:
            PDF content as bytes or None if failed
        """
        try:
            # Get all the required context data
            from core.views import filter_positions, get_country_specific_notice
            from core.models import Interview
            
            # Get positions and filter out empty ones
            positions = employment_ad.positions.all().order_by('order')
            filtered_positions = filter_positions(positions)
            
            # Get interview data
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
            
            # Render HTML content with full context
            html_content = render_to_string(template_name, {
                'ad': employment_ad,
                'positions': filtered_positions,
                'interview_data': interview_data,
                'country_notice': country_notice,
                'pdf_mode': True  # Flag for PDF-specific styling
            })
            
            # Try Playwright first (better quality)
            if self.playwright_available:
                pdf_content = self.generate_pdf_playwright(html_content)
                if pdf_content:
                    return pdf_content
            
            # Fallback to WeasyPrint
            if self.weasyprint_available:
                pdf_content = self.generate_pdf_weasyprint(html_content)
                if pdf_content:
                    return pdf_content
            
            logger.error("No PDF generation method available")
            return None
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return None
    
    def download_pdf_response(self, employment_ad, filename: str = "employment_ad.pdf") -> Optional[HttpResponse]:
        """
        Generate PDF and return as HTTP response for download
        Args:
            employment_ad: EmploymentAd model instance
            filename: Name for the downloaded file
        Returns:
            HttpResponse with PDF content or None if failed
        """
        pdf_content = self.generate_employment_ad_pdf(employment_ad)
        
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        return None


# Global instance
print_service = PrintService()


def generate_employment_ad_pdf(employment_ad) -> Optional[bytes]:
    """Convenience function to generate PDF for employment ad"""
    return print_service.generate_employment_ad_pdf(employment_ad)


def download_employment_ad_pdf(employment_ad, filename: str = "employment_ad.pdf") -> Optional[HttpResponse]:
    """Convenience function to download PDF for employment ad"""
    return print_service.download_pdf_response(employment_ad, filename)
