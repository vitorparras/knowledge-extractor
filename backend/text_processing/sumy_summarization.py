from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os

LANGUAGE = "english"

def summarize_with_sumy(text, method="lsa", sentence_count=3):
    """
    Summarize the given text using the Sumy library.
    
    Args:
        text (str): Text to summarize.
        method (str): Summarization method ('lsa' or 'lex_rank').
        sentence_count (int): Number of sentences to include in the summary.
    
    Returns:
        str: Summarized text.
    """
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    if method == "lsa":
        summarizer = LsaSummarizer(stemmer)
    elif method == "lex_rank":
        summarizer = LexRankSummarizer(stemmer)
    else:
        raise ValueError("Unsupported summarization method. Use 'lsa' or 'lex_rank'.")

    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)
