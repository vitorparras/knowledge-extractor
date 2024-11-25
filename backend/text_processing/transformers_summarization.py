from transformers import T5Tokenizer, T5ForConditionalGeneration

def summarize_with_transformers(text, max_length=150, min_length=40):
    """
    Resume o texto usando Transformers (modelo T5-small).
    :param text: Texto original
    :param max_length: Tamanho máximo do resumo
    :param min_length: Tamanho mínimo do resumo
    :return: Resumo do texto
    """
    try:
        # Inicializar o modelo e o tokenizer
        tokenizer = T5Tokenizer.from_pretrained("t5-small")
        model = T5ForConditionalGeneration.from_pretrained("t5-small")
        # Preparar o texto para entrada no modelo
        input_text = "summarize: " + text
        inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True)

        # Gerar o resumo
        summary_ids = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

    except Exception as e:
        return f"Error during summarization with Transformers: {str(e)}"
