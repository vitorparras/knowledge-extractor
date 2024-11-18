from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def summarize_with_ptt5(text):
    try:
        tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")
        model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")

        inputs = tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        return f"Erro ao resumir com PTT5: {str(e)}"
