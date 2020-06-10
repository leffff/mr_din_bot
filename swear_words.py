from bs4 import BeautifulSoup
from string import punctuation
import requests


def russian_swear_words() -> set:
    URL = 'http://www.russki-mat.net/e/mat_slovar.htm'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_='lem')
    translator = str.maketrans({elem: None for elem in punctuation + '—1234567890'})
    res = set()

    for i in range(0, 116):
        words = results[i].text.split()
        if len(words) == 1:
            res.add(words[0].translate(translator).lower())
    return res
