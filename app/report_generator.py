import os
import io
import urllib.request
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def download_marathi_font():
    """
    Automatically downloads the Poppins font (supports Marathi/Hindi) 
    from Google Fonts repository if it doesn't exist locally.
    """
    font_filename = "poppins.ttf"
    font_url = "https://githubusercontent.com"
    
    if not os.path.exists(font_filename):
        try:
            # इंटरनेटवरून फॉन्ट डाउनलोड करणे
            urllib.request.urlretrieve(font_url, font_filename)
        except Exception:
            pass
    return font_filename

def generate_report(source_file, question, answer):
    """
    Generates a clean PDF report with full Marathi support.
    Fixed the black block error by removing HTML bold tags.
    """
    font_path = download_marathi_font()

    # फॉन्ट रजिस्टर करणे
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont("PoppinsFont", font_path))
            active_font = "PoppinsFont"
        except Exception:
            active_font = "Helvetica"
    else:
        active_font = "Helvetica"

    # मेमरी बफर तयार करणे
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    story = []

    # 🎨 स्टाईल्स (इथे आपण थेट अक्षरांचा आकार मोठा करून ठळक करणार आहोत, टॅग न वापरता)
    title_style = ParagraphStyle(
        'DocTitle',
        fontName=active_font,
        fontSize=22,
        leading=28,
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        fontName=active_font,
        fontSize=14,
        leading=18,
        alignment=1, # Center
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        fontName=active_font,
        fontSize=13,
        leading=18,
        spaceBefore=14,
        spaceAfter=6,
        textColor="#1E3A8A" # नेव्ही ब्लू रंग (दिसायला खूप अट्रॅक्टिव्ह वाटेल)
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        fontName=active_font,
        fontSize=10,
        leading=16,
        spaceAfter=8
    )

    # 📝 पीडीएफ मजकूर भरणे (काळे डब्बे टाळण्यासाठी <b> टॅग पूर्णपणे काढले आहेत)
    story.append(Paragraph("PharmaGen AI Copilot", title_style))
    story.append(Paragraph("Investigation Report", subtitle_style))
    
    story.append(Paragraph(f"Source File: {source_file}", body_style))
    story.append(Spacer(1, 10))

    # User Question Section
    story.append(Paragraph("User Question:", heading_style))
    story.append(Paragraph(question, body_style))
    story.append(Spacer(1, 10))

    # AI Analysis Section
    story.append(Paragraph("AI-Assisted Analysis:", heading_style))
    
    # ओळींचे विश्लेषण करून पॅराग्राफ जोडणे
    lines = answer.split("\n")
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line:
            # जर मुख्य हेडिंग असेल (उदा. ### Possible Root Causes)
            if cleaned_line.startswith("###"):
                heading_text = cleaned_line.replace("###", "").strip()
                story.append(Paragraph(heading_text, heading_style))
            # जर बुलेट पॉईंट असेल
            elif cleaned_line.startswith("-") or cleaned_line.startswith("*"):
                bullet_text = cleaned_line.replace("-", "").replace("*", "").strip()
                story.append(Paragraph(f"• {bullet_text}", body_style))
            else:
                story.append(Paragraph(cleaned_line, body_style))

    story.append(Spacer(1, 15))
    
    # Disclaimer Note
    disclaimer_style = ParagraphStyle('Disc', fontName=active_font, fontSize=8, leading=12, spaceBefore=25)
    story.append(Paragraph("Note: This report is AI-assisted and intended to support human investigation. Final decisions must be made by qualified personnel.", disclaimer_style))

    # पीडीएफ तयार करणे
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
