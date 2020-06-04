from difflib import SequenceMatcher as sm
from string import punctuation as p


def similarity(s: list) -> float:
    cleaner = lambda x: "".join([i for i in x if i not in p])  # лямбда функция для очистки строки от пунктуации
    s = list(map(cleaner, s))  # очистка строки от знаков препинания
    normalized1, normalized2 = s[0].lower(), s[1].lower()  # приведение к нижнему регистру
    matcher = sm(None, normalized1, normalized2)  # вычисление закономернорстей
    return matcher.ratio()  # возвращение процента совпадения
