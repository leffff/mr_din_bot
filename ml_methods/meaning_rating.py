from gensim.models.keyedvectors import Word2VecKeyedVectors
from os import getcwd
from os.path import join
import numpy as np
from scipy import spatial
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from string import punctuation

model = Word2VecKeyedVectors.load(join(getcwd() + "../ml/russian_database"))
STOPWORDS = stopwords.words("russian")
index2word_set = set(model.index2word)
moprh = MorphAnalyzer()

part_of_speech = lambda \
        word: f"{moprh.parse(word)[0].normal_form}_{str(moprh.parse(word)[0].normalized.tag).split(',')[0]}"


def avg_feature_vector(sentence, model, num_features, index2word_set) -> np.ndarray:
    words = sentence.split()
    feature_vec = np.zeros((num_features,), dtype='float32')
    n_words = 0
    for word in words:
        word = part_of_speech(word)
        word = word.replace("INFN", "VERB")
        word = word.replace("ADJF", "ADJ")
        print(word)
        print(word in index2word_set, word.split("_")[-1] != "UNKN")
        if word in index2word_set and word.split("_")[-1] != "UNKN":
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if n_words > 0:
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec


def clean_text(text: str) -> str:
    cleaned = "".join([symbol for symbol in text if symbol not in punctuation])
    cleaned = cleaned.lower()
    cleaned = " ".join([word for word in cleaned.split() if word not in STOPWORDS])
    return cleaned


def distance(v1, v2) -> float:
    sim = 1 - spatial.distance.cosine(v1, v2)
    return sim

# comparison = ['красивый кактус в поле', 'красивая в поле кактус красивый']
# comparison = list(map(clean_text, comparison))

# s1_afv = avg_feature_vector(comparison[0], model=model, num_features=300, index2word_set=index2word_set)
# s2_afv = avg_feature_vector(comparison[1], model=model, num_features=300, index2word_set=index2word_set)
# print(distance(s1_afv, s2_afv))

# sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
# print(sim)
