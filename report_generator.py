from fpdf import FPDF
from datetime import datetime

def generate_report(data, analysis, url):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"AI Web Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"URL: {url}", ln=True)
    pdf.ln(10)
    
    # Website Metadata
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Website Metadata", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Title: {data['title']}")
    pdf.multi_cell(0, 10, txt=f"Description: {data['metadata']['description']}")
    pdf.multi_cell(0, 10, txt=f"Keywords: {data['metadata']['keywords']}")
    pdf.ln(5)
    
    # Content Analysis
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Content Analysis", ln=True)
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Headings Found: {len(data['headings'])}", ln=True)
    pdf.cell(200, 10, txt=f"Paragraphs Found: {len(data['paragraphs'])}", ln=True)
    pdf.cell(200, 10, txt=f"Tables Found: {len(data['tables'])}", ln=True)
    pdf.cell(200, 10, txt=f"Links Found: {len(data['links'])}", ln=True)
    pdf.ln(5)
    
    # AI Insights
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="AI Analysis", ln=True)
    pdf.set_font("Arial", size=12)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, txt="Summary:", ln=False)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=analysis['summary'])
    pdf.ln(3)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, txt="Sentiment:", ln=False)
    pdf.set_font("Arial", size=12)
    sentiment = analysis['sentiment']
    pdf.cell(0, 10, txt=f"{sentiment['label']} (Confidence: {sentiment['score']:.2f})", ln=True)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, txt="Classification:", ln=False)
    pdf.set_font("Arial", size=12)
    classification = analysis['classification']
    pdf.cell(0, 10, txt=f"{classification['labels'][0]} (Score: {classification['scores'][0]:.2f})", ln=True)
    pdf.ln(5)
    
    # Topics and Keywords
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Content Topics", ln=True)
    pdf.set_font("Arial", size=12)
    for topic in analysis['topics']:
        pdf.cell(0, 10, txt=topic, ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Top Keywords", ln=True)
    pdf.set_font("Arial", size=12)
    for keyword, freq in analysis['keyword_density'].items():
        pdf.cell(0, 10, txt=f"- {keyword}: {freq} occurrences", ln=True)
    
    # Accessibility
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Accessibility Score", ln=True)
    pdf.set_font("Arial", size=12)
    acc = data['accessibility']
    pdf.cell(0, 10, txt=f"Images with alt text: {acc['alt_tags']}/{acc['total_images']}", ln=True)
    pdf.cell(0, 10, txt=f"ARIA roles found: {acc['aria_roles']}", ln=True)
    
    return pdf.output(dest='S').encode('latin1')