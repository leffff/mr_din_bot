from bs4 import BeautifulSoup
from urllib.request import urlopen
from string import punctuation


def russian_swear_words():
    translator = str.maketrans({elem: None for elem in punctuation + '—1234567890'})
    res = set()
    bs = BeautifulSoup(urlopen('http://www.russki-mat.net/e/mat_slovar.htm').read(), features="lxml")
    for swear in bs.find_all('span', attrs={'class': 'lem'}):
        words = swear.text.split()
        if len(words) == 1:
            res.add(words[0].translate(translator).lower())
    return res

