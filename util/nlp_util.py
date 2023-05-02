import nltk
import numpy as np
import regex as re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import Set, List, Dict, AnyStr

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')


def preprocess_text(document: AnyStr) -> AnyStr:
    document = re.sub('[^a-zA-Z]', ' ', document)
    document = document.lower()
    return document


def tokenize(document: AnyStr, preprocess=True) -> List:
    wl = WordNetLemmatizer()
    if preprocess:
        document = preprocess_text(document)
    document = document.split()
    document = [wl.lemmatize(word) for word in document if word not in set(stopwords.words('english'))]
    return document


def get_unique_terms(corpus: List) -> Set:
    return set(corpus)


def get_tf(unique_terms: Set, tokens: List) -> Dict:
    tf_dict = {}
    n_terms = len(unique_terms)
    for term in unique_terms:
        count = np.count_nonzero(tokens == term)
        tf = count/n_terms
        tf_dict[term] = tf
    return tf_dict


def get_idf(unique_terms: Set, documents: List[List]) -> Dict:
    idf_dict = {}
    n_docs = len(documents)
    for term in unique_terms:
        count = 0
        for i in range(n_docs):
            if term in documents[i]:
                count += 1
        val = n_docs/(count + 1)
        idf_dict[term] = np.log(val)
    return idf_dict


def get_tfidf(unique_terms: Set, tokens: List, documents: List[List]) -> Dict:
    tf_dict = get_tf(unique_terms, tokens)
    idf_dict = get_idf(unique_terms, documents)
    tfidf_dict = {}
    for term in unique_terms:
        tfidf_dict[term] = {"TF": tf_dict[term], "IDF": idf_dict[term], "TF_IDF": tf_dict[term]*idf_dict[term]}
    return tfidf_dict