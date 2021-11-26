def get_all_words():
    file = 'odm.txt'
    words = []
    with open(file, encoding='utf-8') as f:
        for line in f.readlines():
            words.extend(map(str.strip, line.split(',')))

    return words
