from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """
    Extrai texto de um arquivo PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Erro ao extrair texto do PDF: {str(e)}")
