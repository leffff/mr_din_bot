from gensim.models.keyedvectors import Word2VecKeyedVectors
from os import getcwd
from os.path import join
import numpy as np
from scipy import spatial
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from string import punctuation

model = Word2VecKeyedVectors.load(join("/".join(getcwd().split("/")[:-1]) + "/ml/russian_database"))
STOPWORDS = stopwords.words("russian")
index2word_set = set(model.index2word)
moprh = MorphAnalyzer()


class Similarity:
    def __init__(self, model, index2word_set, num_features=300):
        self.model = model
        print(type(self.model))
        self.itw = index2word_set
        self.num_f = num_features

    def __avg_feature_vector(self, sentence: str) -> np.ndarray:
        words = sentence.split()
        feature_vec = np.zeros((self.num_f), dtype='float32')
        n_words = 0

        part_of_speech = lambda \
                word: f"{moprh.parse(word)[0].normal_form}_{str(moprh.parse(word)[0].normalized.tag).split(',')[0]}"

        for word in words:
            word = part_of_speech(word)
            word = word.replace("INFN", "VERB")
            word = word.replace("ADJF", "ADJ")
            if word in self.itw and word.split("_")[-1] != "UNKN":
                n_words += 1
                feature_vec = np.add(feature_vec, self.model[word])
        if n_words > 0:
            feature_vec = np.divide(feature_vec, n_words)
        return feature_vec

    def __clean_text(self, text: str) -> str:
        cleaned = "".join([symbol for symbol in text if symbol not in punctuation])
        cleaned = cleaned.lower()
        cleaned = " ".join([word for word in cleaned.split() if word not in STOPWORDS])
        return cleaned

    def distance(self, v1: np.ndarray, v2: np.ndarray) -> float:
        sim = 1 - spatial.distance.cosine(v1, v2)
        return sim

    def sim(self, sentences: list) -> float:
        clean = list(map(self.__clean_text, sentences))
        v1 = self.__avg_feature_vector(clean[0])
        v2 = self.__avg_feature_vector(clean[1])
        sim = self.distance(v1, v2)

        return sim


# comparison = ['некрасивое яблоко', 'красивая в поле кактус красивый']
#
# s = Similarity(model, index2word_set)
# print(s.sim(comparison))

# sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
# print(sim)
