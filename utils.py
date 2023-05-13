"""
-----------------------------------------------------------------------
utils.py
-----------------------------------------------------------------------
Common utils that are used across files.

parse_sentences
    Used to decompose documents into 'sentence-like' chunks.

preprocessing
    Used to process the sentences into more managable sentences for
    the vectoriser and model.
"""
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

sws = stopwords.words("english")
ps = PorterStemmer()

def parse_sentences(job):
    sections = job.split("\n")
    sentences = [datum.split(".") for datum in sections]
    decomposed = [datum.strip() for lst in sentences for datum in lst]
    filtered = [datum for datum in decomposed if datum]
    return filtered

def preprocessing(sentence, sws=sws):
    tokenised = word_tokenize(sentence)
    lower = [word.lower() for word in tokenised]
    regex = [re.sub(r"[^a-z0-9][^a-z0-9\+\-]*", "", word) for word in lower]
    filtered = [word for word in regex if word]
    stopwords = [word for word in filtered if word not in sws]
    stemmed = [ps.stem(word) for word in stopwords if word]
    return " ".join(stemmed)
