from transformers import BartTokenizer, BartForConditionalGeneration




def summarize_with_bart(text, max_length=150, min_length=40):
    """
    Resume o texto usando o modelo BART (facebook/bart-large-cnn).
    :param text: Texto original
    :param max_length: Tamanho máximo do resumo
    :param min_length: Tamanho mínimo do resumo
    :return: Resumo do texto
    """
    try:
        
        # Inicializar o modelo e o tokenizer
        tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
        model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        
        # Tokenizar o texto de entrada
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", truncation=True)

        # Gerar o resumo
        summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

    except Exception as e:
        return f"Error during summarization with BART: {str(e)}"
