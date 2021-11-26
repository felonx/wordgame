import re

def get_all_words():
    file = 'odm.txt'
    out = []
    with open(file, encoding='utf-8') as f:
        for line in f.readlines():
            words = map(str.strip, line.split(','))  # split and strip
            # words = map(str.lower, words)            # go lowercase
            pattern = re.compile(r'^[a-ząćęłńśóżź]{2,}$')
            words = filter(pattern.match, words)  # keep only words with 2+ lowercase-letter
            out.extend(words)

    return out
