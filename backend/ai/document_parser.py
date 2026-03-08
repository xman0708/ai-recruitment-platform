import os
import PyPDF2
import docx2txt

def extract_text_from_file(file_path: str) -> str:
    """
    Extracts raw text from PDF, DOCX, or TXT files.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                    
        elif ext == ".docx":
            text = docx2txt.process(file_path)
            
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        
    return text.strip()
