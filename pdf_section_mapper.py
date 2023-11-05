import re
from PyPDF2 import PdfReader

# Function to extract table of contents from PDF
def extract_toc(pdf_path):
    with PdfReader(pdf_path) as pdf:
        toc_text = ""
        # This assumes that the TOC is always on the third page, adjust if necessary
        toc_text += pdf.pages[2].extract_text()
    return toc_text

# Function to create a mapping of section numbers to page numbers
def create_section_mapping(toc_text):
    section_mapping = {}
    lines = toc_text.split('\n')
    for line in lines:
        # Adjust the regex according to the actual format of your TOC
        match = re.search(r'^(\d+)\s+(.*?)\.*\s+(\d+)$', line)
        if match:
            section_number = match.group(1)
            page_number = match.group(3)
            section_mapping[section_number] = int(page_number)
    return section_mapping

# Main function to process PDF and return a section mapping
def get_section_mapping(pdf_path):
    toc_text = extract_toc(pdf_path)
    section_mapping = create_section_mapping(toc_text)
    return section_mapping
