"""
Utility functions for handling file uploads and text extraction.
"""
import os
import tempfile
from pathlib import Path


def extract_text_from_file(file_obj):
    """
    Extract text from various file formats.
    
    Args:
        file_obj: Django UploadedFile object
    
    Returns:
        str: Extracted text from the file
    """
    filename = file_obj.name.lower()
    
    try:
        # Handle plain text files
        if filename.endswith('.txt'):
            return file_obj.read().decode('utf-8')
        
        # Handle PDF files
        elif filename.endswith('.pdf'):
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(file_obj)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                return "Note: PDF support requires PyPDF2 library. Install with: pip install PyPDF2"
        
        # Handle DOCX files
        elif filename.endswith('.docx'):
            try:
                from docx import Document
                doc = Document(file_obj)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                return "Note: DOCX support requires python-docx library. Install with: pip install python-docx"
        
        # Handle DOC files (older Word format)
        elif filename.endswith('.doc'):
            try:
                import python_docx
                # Note: python-docx doesn't support .doc format well
                # For .doc files, recommend converting to .docx first
                return "Note: .doc files are not supported. Please convert to .docx format."
            except ImportError:
                return "Note: Document support requires python-docx library. Install with: pip install python-docx"
        
        else:
            return f"Unsupported file format: {filename}. Supported formats: .txt, .pdf, .docx"
    
    except Exception as e:
        return f"Error extracting text from file: {str(e)}"
