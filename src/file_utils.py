"""Utility functions for file handling."""

from pathlib import Path
from typing import Optional
import tempfile
import os

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import docx2txt
except ImportError:
    docx2txt = None


def read_uploaded_file(uploaded_file) -> str:
    """
    Read content from uploaded file (txt, pdf, or docx).
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Content extracted from the file
    """
    if uploaded_file is None:
        return ""
    
    file_name = uploaded_file.name.lower()
    
    # Handle text files
    if file_name.endswith('.txt'):
        return uploaded_file.read().decode('utf-8', errors='ignore')
    
    # Handle PDF files
    elif file_name.endswith('.pdf'):
        if PdfReader is None:
            raise ImportError("pypdf is required for PDF support. Install with: pip install pypdf")
        
        try:
            pdf_reader = PdfReader(uploaded_file)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text()
            return text_content
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
    
    # Handle DOCX files
    elif file_name.endswith('.docx'):
        if Document is None:
            raise ImportError("python-docx is required for DOCX support. Install with: pip install python-docx")
        
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name
            
            # Read DOCX
            doc = Document(tmp_path)
            text_content = "\n".join([para.text for para in doc.paragraphs])
            
            # Cleanup
            os.unlink(tmp_path)
            return text_content
        except Exception as e:
            raise ValueError(f"Error reading DOCX file: {str(e)}")
    
    else:
        raise ValueError(f"Unsupported file format: {file_name}. Supported formats: .txt, .pdf, .docx")
