"""
cPanel PDF Service - Simplified PDF generation for cPanel hosting
This service provides reliable PDF generation that works on cPanel with minimal dependencies.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse

logger = logging.getLogger(__name__)

# Try to import PDF libraries in order of preference
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger.warning("WeasyPrint not available")

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not available")

class CPanelPDFService:
    """Simplified PDF service optimized for cPanel hosting"""
    
    def __init__(self):
        self.weasyprint_available = WEASYPRINT_AVAILABLE
        self.reportlab_available = REPORTLAB_AVAILABLE
        
        if not self.weasyprint_available and not self.reportlab_available:
            logger.error("No PDF generation library available")
    
    def generate_pdf_weasyprint(self, html_content: str) -> Optional[bytes]:
        """Generate PDF using WeasyPrint (preferred for HTML rendering)"""
        if not self.weasyprint_available:
            return None
        
        try:
            # Configure WeasyPrint for cPanel
            css_string = """
            @page {
                size: A4;
                margin: 0.5cm;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.2;
            }
            """
            
            # Generate PDF
            pdf_bytes = weasyprint.HTML(string=html_content).write_pdf(
                stylesheets=[weasyprint.CSS(string=css_string)],
                optimize_images=True
            )
            
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"WeasyPrint PDF generation failed: {e}")
            return None
    
    def generate_pdf_reportlab(self, employment_ad, positions, interview_data, country_notice) -> Optional[bytes]:
        """Generate PDF using ReportLab (fallback method)"""
        if not self.reportlab_available:
            return None
        
        try:
            from io import BytesIO
            
            # Create PDF buffer
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                 rightMargin=0.5*cm, leftMargin=0.5*cm,
                                 topMargin=0.5*cm, bottomMargin=0.5*cm)
            
            # Register fonts
            try:
                # Try to register custom fonts if available
                font_path = Path(settings.BASE_DIR) / 'core' / 'static' / 'fonts'
                if (font_path / 'Kalimati.ttf').exists():
                    pdfmetrics.registerFont(TTFont('Kalimati', str(font_path / 'Kalimati.ttf')))
                if (font_path / 'olympia-bold.TTF').exists():
                    pdfmetrics.registerFont(TTFont('OlympiaBold', str(font_path / 'olympia-bold.TTF')))
            except Exception as e:
                logger.warning(f"Could not register custom fonts: {e}")
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Create custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6,
                fontName='Helvetica'
            )
            
            # Build PDF content
            story = []
            
            # Title
            title_text = f"{employment_ad.country if employment_ad.country else 'देश'} मा रोजगारी"
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 12))
            
            # Company info
            if employment_ad.company_name:
                company_text = f"Company: {employment_ad.company_name}"
                story.append(Paragraph(company_text, normal_style))
            
            # Meta information
            meta_data = []
            if employment_ad.pre_approval_date:
                meta_data.append(['Pre Approval Date:', str(employment_ad.pre_approval_date)])
            if employment_ad.chalani_no:
                meta_data.append(['Chalani No.:', str(employment_ad.chalani_no)])
            if employment_ad.lot_no:
                meta_data.append(['LOT No.:', str(employment_ad.lot_no)])
            if employment_ad.city:
                meta_data.append(['City:', str(employment_ad.city)])
            
            if meta_data:
                meta_table = Table(meta_data, colWidths=[3*cm, 4*cm])
                meta_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(meta_table)
                story.append(Spacer(1, 12))
            
            # Positions table
            if positions:
                # Table headers
                table_data = [['S.N.', 'Position', 'Male', 'Female', 'Salary', 'Education', 'Contract']]
                
                # Add position data
                for i, position in enumerate(positions, 1):
                    row = [
                        str(i),
                        position.position or '',
                        str(position.male_count or ''),
                        str(position.female_count or ''),
                        str(position.salary_amount or ''),
                        position.min_qualification or '',
                        str(position.contract_duration or '')
                    ]
                    table_data.append(row)
                
                # Create table
                positions_table = Table(table_data, colWidths=[1*cm, 4*cm, 1*cm, 1*cm, 2*cm, 3*cm, 2*cm])
                positions_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(positions_table)
                story.append(Spacer(1, 12))
            
            # Interview information
            if interview_data:
                interview_text = f"Interview Date: {interview_data.get('nepali_date', '')} ({interview_data.get('gregorian_date', '')})"
                if interview_data.get('location'):
                    interview_text += f"<br/>Location: {interview_data.get('location')}"
                story.append(Paragraph(interview_text, normal_style))
                story.append(Spacer(1, 12))
            
            # Country notice
            if country_notice:
                story.append(Paragraph("Important Notice:", normal_style))
                story.append(Paragraph(country_notice, normal_style))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF content
            pdf_content = buffer.getvalue()
            buffer.close()
            
            return pdf_content
            
        except Exception as e:
            logger.error(f"ReportLab PDF generation failed: {e}")
            return None
    
    def generate_employment_ad_pdf(self, employment_ad, template_name: str = "employment_ad_preview.html") -> Optional[bytes]:
        """Generate PDF for employment advertisement"""
        try:
            # Get related data
            positions = employment_ad.positions.all().order_by('order')
            
            # Get interview data
            try:
                from core.models import Interview
                interview = Interview.objects.filter(employment_ad=employment_ad).first()
                interview_data = {
                    'nepali_date': interview.nepali_date if interview else '',
                    'gregorian_date': interview.gregorian_date if interview else '',
                    'location': interview.location if interview else '',
                } if interview else {}
            except:
                interview_data = {}
            
            # Get country notice
            try:
                from core.utils import get_country_specific_notice
                country_notice = get_country_specific_notice(employment_ad.country)
            except:
                country_notice = ""
            
            # Try WeasyPrint first (better HTML rendering)
            if self.weasyprint_available:
                try:
                    # Render HTML template
                    html_content = render_to_string(template_name, {
                        'ad': employment_ad,
                        'positions': positions,
                        'interview_data': interview_data,
                        'country_notice': country_notice,
                        'pdf_mode': True
                    })
                    
                    pdf_content = self.generate_pdf_weasyprint(html_content)
                    if pdf_content:
                        return pdf_content
                except Exception as e:
                    logger.warning(f"WeasyPrint failed, trying ReportLab: {e}")
            
            # Fallback to ReportLab
            if self.reportlab_available:
                pdf_content = self.generate_pdf_reportlab(
                    employment_ad, positions, interview_data, country_notice
                )
                if pdf_content:
                    return pdf_content
            
            logger.error("All PDF generation methods failed")
            return None
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return None
    
    def download_pdf_response(self, employment_ad, filename: str = "employment_ad.pdf") -> Optional[HttpResponse]:
        """Generate PDF and return as HTTP response for download"""
        pdf_content = self.generate_employment_ad_pdf(employment_ad)
        
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        return None

# Global instance
cpanel_pdf_service = CPanelPDFService()
