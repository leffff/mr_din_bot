def russian_swear_words() -> set:
    with open("ml/russian_swear_words.txt", "r") as fin:
        swear_words = set(fin.read().split(", "))
    return swear_words
