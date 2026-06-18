"""
LandScope AI — PDF Parser.
Parses master plan documents and extracts relevant text.
"""
import PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF document."""
    text_content = []
    try:
        # PyMuPDF is imported as fitz usually, wait let's use fitz
        import fitz
        doc = fitz.open(file_path)
        for page in doc:
            text_content.append(page.get_text())
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return ""

def extract_projects_from_master_plan(pdf_text: str) -> list[dict]:
    """
    Extract potential projects from master plan text.
    In a full implementation, this would pass chunks to the LLM
    to extract structured JSON using function calling.
    """
    # Placeholder logic
    projects = []
    if "Metro" in pdf_text:
        projects.append({
            "name": "New Metro Extension",
            "type": "transport",
            "status": "planned"
        })
    return projects
