import nltk
import numpy as np
import regex as re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import Set, List, Dict, AnyStr
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

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
    tokens = np.array(tokens)
    tf_dict = {}
    n_terms = len(unique_terms)
    for term in tqdm(unique_terms):
        count = np.count_nonzero(tokens == term)
        tf = count / n_terms
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
        val = n_docs / (count + 1)
        idf_dict[term] = np.log(val)
    return idf_dict


def get_tfidf(unique_terms: Set, tokens: List, documents: List[List]) -> Dict:
    tfidf_dict = {}
    n_terms = len(unique_terms)
    n_docs = len(documents)
    for term in tqdm(unique_terms):
        tf_count = np.count_nonzero(np.array(tokens) == term)
        tf_value = tf_count / n_terms
        idf_count = 0
        for i in range(n_docs):
            if term in documents[i]:
                idf_count += 1
        idf_value = n_docs / (idf_count + 1)
        idf_value = np.log(idf_value)
        tfidf_dict[term] = {"TF": tf_value, "IDF": idf_value, "TF_IDF": tf_value * idf_value}
    return tfidf_dict


def tf_idf_sklearn(documents, max_df=1, min_df=1, max_features=100):
    vectorizer = TfidfVectorizer(analyzer='word', stop_words='english',
                                 max_features=max_features,
                                 max_df=max_df, min_df=min_df)
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer
