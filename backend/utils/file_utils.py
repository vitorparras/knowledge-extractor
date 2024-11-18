import os
import textract
from werkzeug.utils import secure_filename

# Tipos de arquivos suportados
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "mp3", "wav"}

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return "." in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS

def get_file_extension(filepath):
    """Obtém a extensão de um arquivo."""
    return os.path.splitext(filepath)[1][1:].lower()

def read_text_file(filepath):
    """
    Lê o conteúdo de um arquivo de texto, PDF ou Word.
    Retorna o conteúdo como uma string.
    """
    try:
        content = textract.process(filepath).decode("utf-8")
        return content
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o arquivo {filepath}: {str(e)}")
