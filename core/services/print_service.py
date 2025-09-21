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

try:
    import reportlab
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not available. Install with: pip install reportlab")


class PrintService:
    """Service for generating high-quality PDFs from employment ad previews"""
    
    def __init__(self):
        self.playwright_available = PLAYWRIGHT_AVAILABLE
        self.weasyprint_available = WEASYPRINT_AVAILABLE
        self.reportlab_available = REPORTLAB_AVAILABLE
        
        if not self.playwright_available and not self.weasyprint_available and not self.reportlab_available:
            logger.error("No PDF generation library available. Install either Playwright, WeasyPrint, or ReportLab.")
    
    def generate_pdf_playwright(self, html_content: str, filename: str = "employment_ad.pdf") -> Optional[bytes]:
        """
        Generate PDF using Playwright with professional-grade settings for InDesign-level quality
        Returns PDF content as bytes or None if failed
        """
        if not self.playwright_available:
            logger.error("Playwright not available")
            return None
        
        try:
            with sync_playwright() as p:
                # Launch browser with professional newspaper printing settings
                browser = p.chromium.launch(
                    args=[
                        '--force-device-scale-factor=3',  # 300 DPI rendering for newspaper quality
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor',
                        '--enable-font-antialiasing',
                        '--disable-background-timer-throttling',
                        '--disable-backgrounding-occluded-windows',
                        '--disable-renderer-backgrounding',
                        '--font-render-hinting=none',  # Disable font hinting for crisp text
                        '--disable-font-subpixel-positioning',  # Better text rendering
                        '--enable-gpu-rasterization',
                        '--enable-zero-copy',
                        '--disable-gpu-sandbox',
                        '--high-dpi-support=1',  # Enable high DPI support
                        '--force-color-profile=srgb',  # Consistent color profile
                        '--disable-features=TranslateUI',  # Disable unnecessary features
                        '--disable-ipc-flooding-protection'  # Better performance
                    ]
                )
                
                # Create page with professional newspaper printing viewport
                page = browser.new_page(
                    viewport={'width': 3720, 'height': 5262},  # A4 at 450 DPI for newspaper quality
                    device_scale_factor=3  # 3x scaling for ultra-crisp rendering
                )
                
                # Set content and wait for fonts to load
                page.set_content(html_content, wait_until="networkidle")
                
                # Wait for fonts and images to fully load
                page.wait_for_timeout(2000)
                
                # Wait for all images to load
                page.wait_for_function("() => Array.from(document.images).every(img => img.complete)")
                
                # Generate PDF with professional newspaper printing settings
                pdf_content = page.pdf(
                    format="A4",
                    print_background=True,
                    margin={
                        "top": "0.2cm",  # Minimal margins for maximum content
                        "right": "0.2cm", 
                        "bottom": "0.2cm",
                        "left": "0.2cm"
                    },
                    scale=1.0,  # No scaling to maintain exact dimensions
                    prefer_css_page_size=True,
                    display_header_footer=False,
                    tagged=True,  # Enable PDF tags for accessibility
                    outline=True,  # Enable PDF outline
                    width="210mm",  # Exact A4 width
                    height="297mm"   # Exact A4 height
                )
                
                browser.close()
                return pdf_content
                
        except Exception as e:
            logger.error(f"Playwright PDF generation failed: {e}")
            return None
    
    def generate_pdf_weasyprint(self, html_content: str, filename: str = "employment_ad.pdf") -> Optional[bytes]:
        """
        Generate PDF using WeasyPrint with professional print settings
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
                # Professional CSS for newspaper-quality PDF generation
                professional_css = weasyprint.CSS(string="""
                    @page {
                        size: A4;
                        margin: 0.2cm;
                        bleed: 0.3cm;
                        marks: crop cross;
                        color-adjust: exact;
                        resolution: 450dpi;
                    }
                    
                    * {
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                        text-shadow: none !important;
                        -webkit-text-stroke: none !important;
                        filter: none !important;
                        backdrop-filter: none !important;
                    }
                    
                    body {
                        font-smooth: always;
                        -webkit-font-smoothing: antialiased;
                        -moz-osx-font-smoothing: grayscale;
                        text-rendering: optimizeLegibility;
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges;
                        image-rendering: pixelated;
                    }
                    
                    img {
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges;
                        image-rendering: pixelated;
                    }
                    
                    /* Ensure sharp text rendering - Remove all shadows and strokes */
                    h1, h2, h3, h4, h5, h6, p, span, div, td, th, li {
                        text-rendering: optimizeLegibility;
                        font-smooth: always;
                        -webkit-font-smoothing: antialiased;
                        -moz-osx-font-smoothing: grayscale;
                        text-shadow: none !important;
                        -webkit-text-stroke: none !important;
                        filter: none !important;
                    }
                    
                    /* High-quality font rendering */
                    @font-face {
                        font-display: swap;
                        font-smooth: always;
                        -webkit-font-smoothing: antialiased;
                        -moz-osx-font-smoothing: grayscale;
                    }
                """)
                
                # Generate PDF with newspaper-quality settings
                pdf_doc = weasyprint.HTML(filename=temp_html_path)
                pdf_content = pdf_doc.write_pdf(
                    stylesheets=[professional_css],
                    optimize_images=False,  # Don't optimize images to maintain quality
                    jpeg_quality=100,  # Maximum JPEG quality
                    png_quality=100,   # Maximum PNG quality
                    # Additional settings for professional printing
                    base_url=None,  # Prevent external resource loading issues
                    presentational_hints=True  # Better CSS support
                )
                return pdf_content
            finally:
                # Clean up temporary file
                os.unlink(temp_html_path)
                
        except Exception as e:
            logger.error(f"WeasyPrint PDF generation failed: {e}")
            return None
    
    def generate_pdf_reportlab(self, employment_ad, template_name: str = "employment_ad_preview.html") -> Optional[bytes]:
        """
        Generate PDF using ReportLab (cPanel-compatible method)
        Returns PDF content as bytes or None if failed
        """
        if not self.reportlab_available:
            logger.error("ReportLab not available")
            return None
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from io import BytesIO
            
            # Create PDF in memory
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(f"Employment Advertisement - {employment_ad.company_name}", title_style))
            story.append(Spacer(1, 20))
            
            # Company Information
            company_data = [
                ['Company Name:', employment_ad.company_name or 'N/A'],
                ['Country:', employment_ad.country or 'N/A'],
                ['Pre-approval Date:', employment_ad.pre_approval_date or 'N/A'],
                ['Chalani No:', employment_ad.chalani_no or 'N/A'],
                ['LOT No:', employment_ad.lot_no or 'N/A'],
            ]
            
            company_table = Table(company_data, colWidths=[4*cm, 8*cm])
            company_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(company_table)
            story.append(Spacer(1, 20))
            
            # Job Positions
            positions = employment_ad.positions.all().order_by('order')
            if positions:
                story.append(Paragraph("Job Positions", styles['Heading2']))
                story.append(Spacer(1, 10))
                
                # Position table headers
                position_headers = ['Position', 'Male', 'Female', 'Salary', 'Currency']
                position_data = [position_headers]
                
                for pos in positions:
                    if pos.position:  # Only add non-empty positions
                        position_data.append([
                            pos.position or 'N/A',
                            str(pos.male_count or 0),
                            str(pos.female_count or 0),
                            str(pos.salary_amount or 'N/A'),
                            pos.salary_currency or 'N/A'
                        ])
                
                if len(position_data) > 1:  # If we have data beyond headers
                    position_table = Table(position_data, colWidths=[4*cm, 2*cm, 2*cm, 2*cm, 2*cm])
                    position_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(position_table)
            
            # Build PDF
            doc.build(story)
            pdf_content = buffer.getvalue()
            buffer.close()
            return pdf_content
            
        except Exception as e:
            logger.error(f"ReportLab PDF generation failed: {e}")
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
            
            # Add base64 encoded images for PDF generation
            import base64
            import os
            
            # Create a copy of the employment_ad object with base64 image data
            ad_with_base64 = employment_ad
            if hasattr(employment_ad, 'company_banner_image') and employment_ad.company_banner_image:
                try:
                    # Read image with maximum quality preservation
                    with open(employment_ad.company_banner_image.path, 'rb') as img_file:
                        img_data = img_file.read()
                        # Convert to base64 with maximum quality
                        ad_with_base64.company_banner_image_base64 = base64.b64encode(img_data).decode('utf-8')
                        logger.info(f"Banner image encoded successfully: {len(img_data)} bytes")
                except Exception as e:
                    logger.warning(f"Could not encode banner image: {e}")
                    ad_with_base64.company_banner_image_base64 = None
            else:
                ad_with_base64.company_banner_image_base64 = None
                
            if hasattr(employment_ad, 'company_logo_image') and employment_ad.company_logo_image:
                try:
                    # Read image with maximum quality preservation
                    with open(employment_ad.company_logo_image.path, 'rb') as img_file:
                        img_data = img_file.read()
                        # Convert to base64 with maximum quality
                        ad_with_base64.company_logo_image_base64 = base64.b64encode(img_data).decode('utf-8')
                        logger.info(f"Logo image encoded successfully: {len(img_data)} bytes")
                except Exception as e:
                    logger.warning(f"Could not encode logo image: {e}")
                    ad_with_base64.company_logo_image_base64 = None
            else:
                ad_with_base64.company_logo_image_base64 = None
            
            # Render HTML content with full context and high-quality settings
            html_content = render_to_string(template_name, {
                'ad': ad_with_base64,
                'positions': filtered_positions,
                'interview_data': interview_data,
                'country_notice': country_notice,
                'pdf_mode': True,  # Flag for PDF-specific styling
                'high_quality': True,  # Flag for maximum quality rendering
                'print_optimized': True  # Flag for print optimization
            })
            
            # Try Playwright first (better quality)
            if self.playwright_available:
                pdf_content = self.generate_pdf_playwright(html_content)
                if pdf_content:
                    return pdf_content
            
            # Try WeasyPrint (good HTML rendering)
            if self.weasyprint_available:
                pdf_content = self.generate_pdf_weasyprint(html_content)
                if pdf_content:
                    return pdf_content
            
            # Skip ReportLab fallback - it creates a different layout
            # Instead, try to force WeasyPrint installation
            logger.warning("Playwright and WeasyPrint not available. PDF generation may fail.")
            logger.warning("Please install WeasyPrint: pip install weasyprint")
            
            # Only use ReportLab as absolute last resort
            if self.reportlab_available:
                logger.warning("Using ReportLab fallback - this will create a simplified layout")
                pdf_content = self.generate_pdf_reportlab(employment_ad)
                if pdf_content:
                    return pdf_content
            
            # Final fallback to cPanel PDF service
            try:
                from .cpanel_pdf_service import cpanel_pdf_service
                pdf_content = cpanel_pdf_service.generate_employment_ad_pdf(employment_ad, template_name)
                if pdf_content:
                    logger.info("Used cPanel PDF service fallback")
                    return pdf_content
            except Exception as e:
                logger.warning(f"cPanel PDF service fallback failed: {e}")
            
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
