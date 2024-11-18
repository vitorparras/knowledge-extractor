from gensim.summarization import summarize

def summarize_with_gensim(text):
    try:
        summary = summarize(text, ratio=0.2)
        return summary
    except Exception as e:
        return f"Erro ao resumir com Gensim: {str(e)}"
