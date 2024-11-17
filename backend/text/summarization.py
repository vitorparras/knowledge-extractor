from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_summarization_model():
    """
    Carrega o modelo T5 para sumarização.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")
        model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")
        return tokenizer, model
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar modelo de sumarização: {str(e)}")

def summarize_text(text, tokenizer, model, max_length=150):
    """
    Realiza a sumarização de um texto usando o modelo T5.
    """
    try:
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=max_length, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        raise RuntimeError(f"Erro ao sumarizar texto: {str(e)}")
