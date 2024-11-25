from collections import Counter
import spacy




def summarize_with_spacy(text, sentence_limit=3):
    """
    Resume o texto usando SpaCy, selecionando as sentenças mais relevantes.
    :param text: Texto original
    :param sentence_limit: Número de sentenças no resumo
    :return: Resumo do texto
    """
    try:
        
        # Carregar o modelo SpaCy
        nlp = spacy.load("pt_core_news_sm")
        
        # Processar o texto com SpaCy
        doc = nlp(text)

        # Criar um contador de palavras (frequência)
        words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
        word_freq = Counter(words)

        # Calcular pontuação das sentenças com base na frequência de palavras
        sentence_scores = {}
        for sent in doc.sents:
            for word in sent:
                if word.text.lower() in word_freq:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word.text.lower()]

        # Selecionar as sentenças com maior pontuação
        ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        summary = " ".join([sent.text for sent in ranked_sentences[:sentence_limit]])

        return summary

    except Exception as e:
        return f"Error during summarization: {str(e)}"
