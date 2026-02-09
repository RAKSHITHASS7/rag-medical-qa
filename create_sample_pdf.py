"""Create a sample medical PDF for testing."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

def create_sample_medical_pdf():
    """Create a sample medical PDF for testing."""
    output_path = Path("data/pdfs/sample_medical_guide.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Medical Knowledge Guide")
    
    # Page 1: Diabetes
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 100, "Diabetes Mellitus")
    
    c.setFont("Helvetica", 12)
    text = [
        "Diabetes is a chronic metabolic disorder characterized by high blood sugar levels.",
        "There are two main types:",
        "1. Type 1 Diabetes: Autoimmune condition where the body doesn't produce insulin.",
        "2. Type 2 Diabetes: Body becomes resistant to insulin or doesn't produce enough.",
        "",
        "Common symptoms include:",
        "- Excessive thirst and urination",
        "- Increased hunger",
        "- Fatigue",
        "- Blurred vision",
        "- Slow-healing sores",
        "",
        "Treatment typically involves:",
        "- Blood sugar monitoring",
        "- Medication (metformin, insulin)",
        "- Diet and exercise",
        "- Regular medical checkups"
    ]
    
    y = height - 130
    for line in text:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    
    # Page 2: Hypertension
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Hypertension (High Blood Pressure)")
    
    c.setFont("Helvetica", 12)
    text = [
        "Hypertension is a condition where blood pressure is consistently elevated.",
        "Normal blood pressure is below 120/80 mmHg.",
        "Hypertension is defined as 140/90 mmHg or higher.",
        "",
        "Risk factors include:",
        "- Age (risk increases with age)",
        "- Family history",
        "- Obesity",
        "- Lack of physical activity",
        "- High salt intake",
        "- Alcohol consumption",
        "",
        "Treatment options:",
        "- Lifestyle modifications (diet, exercise)",
        "- ACE inhibitors",
        "- Beta-blockers",
        "- Diuretics",
        "- Calcium channel blockers"
    ]
    
    y = height - 80
    for line in text:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    
    # Page 3: Cardiovascular Disease
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Cardiovascular Disease")
    
    c.setFont("Helvetica", 12)
    text = [
        "Cardiovascular disease refers to conditions affecting the heart and blood vessels.",
        "",
        "Common types include:",
        "- Coronary artery disease",
        "- Heart failure",
        "- Arrhythmias",
        "- Valvular heart disease",
        "",
        "Risk factors:",
        "- High blood pressure",
        "- High cholesterol",
        "- Diabetes",
        "- Smoking",
        "- Obesity",
        "- Sedentary lifestyle",
        "",
        "Prevention strategies:",
        "- Regular exercise",
        "- Healthy diet",
        "- Smoking cessation",
        "- Weight management",
        "- Regular health screenings"
    ]
    
    y = height - 80
    for line in text:
        c.drawString(50, y, line)
        y -= 20
    
    c.save()
    print(f"✅ Created sample PDF: {output_path}")

if __name__ == "__main__":
    create_sample_medical_pdf()




