from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import spacy

def load_model(model_name):
    try:
        if model_name == "t5":
            tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")
            model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")
            return tokenizer, model
        elif model_name == "spacy":
            nlp = spacy.load("pt_core_news_sm")
            return nlp
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    except Exception as e:
        raise RuntimeError(f"Error loading model {model_name}: {str(e)}")
