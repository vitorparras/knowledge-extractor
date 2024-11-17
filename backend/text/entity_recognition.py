import spacy

def load_ner_model():
    """
    Carrega o modelo spaCy para reconhecimento de entidades.
    """
    try:
        nlp = spacy.load("pt_core_news_sm")
        return nlp
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar modelo de NER: {str(e)}")

def extract_entities(text, nlp):
    """
    Extrai entidades nomeadas de um texto usando o modelo spaCy.
    """
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        raise RuntimeError(f"Erro ao extrair entidades: {str(e)}")
