import re
import string

def clean_text(text):
    """
    Limpa o texto removendo caracteres especiais e múltiplos espaços.
    """
    text = re.sub(r'\s+', ' ', text)  # Remove múltiplos espaços
    text = re.sub(r'\[.*?\]', '', text)  # Remove conteúdo entre colchetes
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove pontuação
    return text.strip()

def tokenize_text(text):
    """
    Divide o texto em palavras individuais.
    """
    return text.split()

def preprocess_text(raw_text):
    """
    Realiza o pré-processamento completo de um texto.
    """
    cleaned_text = clean_text(raw_text)
    tokens = tokenize_text(cleaned_text)
    return tokens
